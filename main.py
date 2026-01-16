from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from createuser import User
from addproduct import product
from database import user_collection as userTable, product_collection as productTable,cart_collection as cartTable
from security import hash_password,verify_password,encode_response,decode_response
from update import updateuser,updateproduct
from fastapi import FastAPI, HTTPException
from bson import ObjectId
from filter import filterproduct
from cart import addcart



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def roor():
    return{"ststus":"agro is working"}

#add user
@app.post("/adduser")
async def create(user: User):
    user_dict = user.dict()
    user_dict["password"] = hash_password(user_dict["password"])
    await userTable.insert_one(user_dict)
    return {"message": "User added successfully"}

#add product
@app.post("/addproduct")
async def addproduct(product:product):
       product_dict = product.dict()
       await productTable.insert_one(product_dict)
       return{"message":"prodcuct added successfully"}

#fetch all products
@app.get("/products")
async def get_products():
    products = []

    async for product in productTable.find():
        products.append({
            
            "id": str(encode_response((product["_id"]))),
            "product_name": product.get("Product_name"),
            "price": product.get("price"),
            "quantity": product.get("quantity"),
            "description": product.get("description"),
            "image":product.get("image"),
            "seller_id":encode_response(product.get("user_id")) 
        })

    return products

#fetch single product
@app.get("/products/{product_id}")
async def get_product_by_id(product_id: str):
    product_id = decode_response(product_id)
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product = await productTable.find_one({"_id": ObjectId(product_id)})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "id": str(encode_response((product["_id"]))),
        "product_name": product.get("Product_name"),
        "price": product.get("price"),
        "quantity": product.get("quantity"),
        "description": product.get("description"),
        "image_url": product.get("image_url"),
        "seller_id": encode_response(product.get("user_id"))
    }
#fetch user by id 
@app.get("/user/{user_id}")
async def get_user_by_id(user_id:str):
    user_id = decode_response(user_id)
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="invalid user id")
    
    user=await userTable.find_one({"_id" : ObjectId(user_id)})

    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    return {
        "seller_id":str(encode_response(user["_id"])),
        "seller_name":user.get("name"),
        "seller_email":user.get("email"),
        "seller_phone_no":user.get("number"),
        "seller_address":user.get("address"),
        "seller_pincode":user.get("pincode")
    }

#fetch users by role
@app.get("/fetchusers/{role}")
async def fetch_users_by_role(role: str):
    users = []
    cursor = userTable.find({"role": role})

    async for u in cursor:
        users.append({
            "id": str(encode_response(u["_id"])),
            "name": u.get("name"),
            "email": u.get("email"),
            "number": u.get("number"),
            "address": u.get("address"),
            "pincode": u.get("pincode")
        })

    return users

#delete product by id
@app.delete("/deleteproduct/{product_id}")
async def delete_product(product_id:str):
    product_id = decode_response(product_id)
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="invalid product id")

    result = await productTable.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count==0:
        raise HTTPException(status_code=404,detail="product not found")
    
    return{"message":"product deleted successfully"}


#delete user by id 
@app.delete("/deleteuser/{user_id}")
async def delete_user(user_id:str):
    user_id = decode_response(user_id)
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="invalid user id")
    result=await userTable.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count==0:
        raise HTTPException(status_code=404, detail="user not found")
    return{"message":"user deleted successfully"}

#login user
@app.post("/login")
async def login_user(number:str,password:str):
    h_password = hash_password(password)
    user = await userTable.find_one({"number": number})

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    if not verify_password(password,user['password']):
        raise HTTPException(status_code=401, detail="invalid credentials")

    return{"message":"login successfully","user_id":str(encode_response(user["_id"]))}


#update user details
@app.put("/updateuser/{user_id}")
async def update_user(user_id,updateuser:updateuser):
    user_id = decode_response(user_id)
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=404, detail="invalid user id")
    user = await userTable.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    # Extract only sent fields
    data = updateuser.dict(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail="No data provided for update")

    # Update balance
    result = await userTable.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": data}
    )

    return {
        "message": "Balance updated successfully",
        "updated_fields": data
    }


#update product details
@app.put("/updateproduct/{product_id}")
async def update_product(product_id,update_product:updateproduct):
    product_id = decode_response(product_id)
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="invalid product id")
    product = await productTable.find_one({"_id": ObjectId(product_id)})

    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    
    data = update_product.dict(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="no data provided for update")

    result = await productTable.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": data}
    )
    return{
        "message":"product updated successfully",
        "updated fields":data
    }


#filter products
@app.post("/filterproducts")
async def filter_products(filter:filterproduct):
    query={}

    if filter.min_price is not None:
        query['price']={'$gte': filter.min_price}

    if filter.max_price is not None:
        query['price']={'$lte': filter.max_price}

    if filter.min_quantity is not None:
        query['quantity']={'$gte': filter.min_quantity}

    if filter.max_quantity is not None:
        query['quantity']={'$lte': filter.max_quantity}

    if filter.product_name is not None:
        query['product_name']={'$regex': f".*{filter.product_name}.*", '$options': 'i'}

    products = []
    cursor = productTable.find(query)

    async for p in cursor:
        products.append({
            "id": str(encode_response(p["_id"])),
            "product_name": p.get("Product_name"),
            "price": p.get("price"),
            "quantity": p.get("quantity"),
            "seller_id": encode_response(p.get("user_id")),
            "seller_pincode": p.get("pincode")
        })

    return products


#fetch all users
@app.get("/users")
async def get_users():
    users = []
    full_table = userTable.find()
    async for user in full_table:
        users.append({
            "id": str (encode_response((user["_id"]))),
            "name": user.get("name"),
            "number": user.get("number"),
            "email": user.get("email"),
            "role": user.get("role"),
            "address": user.get("address"),
            "pincode":user.get("pincode")

        })

    return users

#add cart item 
@app.post("/addcart")
async def add_cart_item(cart:addcart):
    cart_dict = cart.dict()
    await cartTable.insert_one(cart_dict)
    return{"message":"item added to cart successfully"}

#fetch cart item by user id 
@app.get("/cart/{user_id}")
async def get_cart_by_user_id(user_id:str):
    user_id = decode_response(user_id)
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="invalid user id")
    
    cart_items=[]
    data = cartTable.find({"user_id":user_id})
    async for item in data:
        cart_items.append({
            "cart_id":str(encode_response((item["_id"]))),
            "product_id":encode_response(item.get("product_id"))
        })
    return cart_items

#remove cart
@app.delete("/removecart/{cart_id}")
async def removecart(cart_id:str):
    cart_id = decode_response(cart_id)
    if not ObjectId.is_valid(cart_id):
        raise HTTPException(status_code=400 , detail="invalid cart")
    
    result = await cartTable.delete_one(({"_id": ObjectId(cart_id)}))

    if result.deleted_count==0: 
        raise HTTPException(status_code="cart not found")
    
    return({"message":"cart removed successfully"})

