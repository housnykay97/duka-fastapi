from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from data_schemas import ProductRequest, ProductResponse, PurchaseRequest, PurchaseResponse, SaleRequest, SaleResponse, SalesDetailRequest, SalesDetailResponse, PaymentRequest, PaymentResponse
from models import Base, Product, User, Purchase, Sale, SalesDetail, Payment
from sqlalchemy import create_engine, select

app = FastAPI()

# create a connection to the database using sqlalchemy engine
engine = create_engine("sqlite:///./duka_fastapi.db", echo=True)

# create tables into the database using sqlalchemy 
Base.metadata.create_all(engine)

# create a session to do sql transactions
session = Session(engine)


@app.get("/")
def home():
    return {"Duka FastAPI Version": "1.0"}


def add_user():
    user = User(full_name="Hussna",email="husna1@gmail.com",phone_number="254700539097",password="1234")
    session.add(user)
    session.commit()

#add_user()    

# PRODUCTS
@app.post("/products", response_model=ProductResponse)
def create_product(prod: ProductRequest):
    
    # Store in the database
    dbprod = Product(
        user_id=prod.user_id,
        product_name=prod.product_name,
        buying_price=prod.buying_price,
        selling_price=prod.selling_price,
        stock_quantity=prod.stock_quantity
    )

    session.add(dbprod)
    session.commit()
    return dbprod

@app.get("/products", response_model=list[ProductResponse])
def get_products():
    query = select(Product)
    products = session.scalars(query)
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_single_product(product_id):
    query = select(Product).where(Product.id == product_id)
    product = session.scalars(query).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id : int, prod : ProductRequest ):
    query = select(Product).where(Product.id == product_id)
    product = session.scalars(query).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.product_name = prod.product_name
    product.buying_price = prod.buying_price
    product.selling_price = prod.selling_price
    product.stock_quantity = prod.stock_quantity

    session.commit()
    return product



# End Product Routes

# PURCHASE
@app.post("/purchases", response_model=PurchaseResponse)
def create_purchase(pur: PurchaseRequest):
    dbpurchase = Purchase(
        user_id = pur.user_id,
        product_id = pur.product_id,
        total_cost = pur.total_cost
    )

    session.add(dbpurchase)
    session.commit()
    return dbpurchase

@app.get("/purchases", response_model=list[PurchaseResponse])
def get_purchases():
    query = select(Purchase)
    purchases = session.scalars(query)
    return purchases

# End Purchase Routes

#SALE
@app.post("/sales", response_model=SaleResponse)
def create_sale(sl: SaleRequest):
    dbsale = Sale(
        user_id = sl.user_id
    )

    session.add(dbsale)
    session.commit()
    return dbsale

@app.get("/sales", response_model=list[SaleResponse])
def get_sale():
    query = select(Sale)
    sales = session.scalars(query)
    return sales

# End Sale Routes

# SALESDETAIL
@app.post("/salesdetails", response_model=SalesDetailResponse)
def create_sales_details(sd: SalesDetailRequest):
    s_detail = SalesDetail(
        product_id = sd.product_id,
        sale_id = sd.sale_id,
        quantity = sd.quantity
    )

    session.add(s_detail)
    session.commit()
    return s_detail

@app.get("/salesdetails", response_model=list[SalesDetailResponse])
def get_sales_details():
    query = select(SalesDetail)
    detail = session.scalars(query)
    return detail

# End SalesDetail Routes

# PAYMENT
@app.post("/payments", response_model=PaymentResponse)
def create_payments(pay: PaymentRequest):
    dbpayment = Payment(
        sale_id = pay.sale_id,
        amount_paid = pay.amount_paid,
        transaction_code = pay.transaction_code,
        mrid = pay.mrid,
        crid = pay.crid,
        status = pay.status,
        phone_number = pay.phone_number
        # created_at: datetime
    )

    session.add(dbpayment)
    session.commit()
    return dbpayment

@app.get("/payments", response_model=list[PaymentResponse])
def get_payments():
    query = select(Payment)
    payments = session.scalars(query)
    return payments

# End Payments Routes   