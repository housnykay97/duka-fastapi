from pydantic import BaseModel

class ProductRequest(BaseModel):
    user_id : int
    product_name : str
    buying_price : float
    selling_price : float
    stock_quantity : int

class ProductResponse(BaseModel):
    id : int
    user_id : int
    product_name : str
    buying_price : float
    selling_price : float
    stock_quantity : int


class UserRequest(BaseModel):
    full_name : str
    email : str
    phone_number : str
    password : str

class UserResponse(BaseModel):
    id : int
    full_name : str
    email : str
    phone_number : str
    password : str


    