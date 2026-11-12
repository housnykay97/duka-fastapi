from pydantic import BaseModel, ConfigDict


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


class PurchaseRequest(BaseModel):
    user_id : int
    product_id : int
    total_cost : float

class PurchaseResponse(BaseModel):
    id : int
    user_id : int
    product_id : int
    total_cost : float


class SaleRequest(BaseModel):
    user_id : int    

class SaleResponse(BaseModel):
    id : int
    user_id : int


class SalesDetailRequest(BaseModel):
    product_id : int
    sale_id : int
    quantity : int

class SalesDetailResponse(BaseModel):
    id : int
    product_id : int
    sale_id : int
    quantity : int


class PaymentRequest(BaseModel):
    sale_id : int
    amount_paid : float
    transaction_code : str
    mrid : str
    crid : str
    status : str
    phone_number : str
    # created_at: datetime

class PaymentResponse(BaseModel):
    id : int
    sale_id : int
    amount_paid : float
    transaction_code : str
    mrid : str
    crid : str
    status : str
    phone_number : str
    # created_at : datetime
        


    