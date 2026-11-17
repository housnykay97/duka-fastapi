from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from data_schemas import ProductRequest, ProductResponse, PurchaseRequest, PurchaseResponse, SaleRequest, SaleResponse, SalesDetailRequest, SalesDetailResponse, PaymentRequest, PaymentResponse
from models import Base, Product, User, Purchase, Sale, SalesDetail, Payment
from sqlalchemy import create_engine, select

from myjwt import create_access_token, verify_password, get_current_user


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


# PRODUCTS ROUTES
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
    return session.scalars(query).all


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
    session.refresh(product)
    return product

# End Product Routes


# PURCHASE ROUTES
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


@app.get("/purchases{purchase_id}", response_model=PurchaseResponse)
def get_single_purchase(purchase_id):
    query = select(Purchase).where(Purchase.id == purchase_id)
    purchase = session.scalars(query).first()
    if purchase is None:
        raise HTTPException(
            status_code=404,
            detail="Purchase not found"
        )
    return purchase


@app.put("/purchases/{purchase_id}", response_model=PurchaseResponse)
def update_purchase(purchase_id : int, pur : PurchaseRequest):
    query = select(Purchase).where(Purchase.id == purchase_id)
    purchase = session.scalars(query).first()
    if purchase is None:
        raise HTTPException(
            status_code=404,
            detail="Purchase not found"
        )

    purchase.product_id = pur.product_id
    purchase.total_cost = pur.total_cost

    session.ommit()
    session.refresh(purchase)
    return purchase

# End Purchase Routes


#SALE ROUTES
@app.post("/sales", response_model=SaleResponse)
def create_sale(sl: SaleRequest):
    dbsale = Sale(
        user_id = sl.user_id
    )

    session.add(dbsale)
    session.commit()
    return dbsale


@app.get("/sales", response_model=list[SaleResponse])
def get_sales():
    query = select(Sale)
    sales = session.scalars(query)
    return sales


@app.get("/sales/{sale_id}", response_model=SaleResponse)
def get_single_sale(sale_id):
    query = select(Sale).where(Sale.id == sale_id)
    sale = session.scalars(query).first()
    if sale is None:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )
    return sale


@app.put("/sales/{sale_id}", response_model=SaleResponse)
def update_sale(sale_id : int, sl : SaleRequest):
    query = select(Sale).where(Sale.id == sale_id)
    sale = session.scalars(query).first()
    if sale is None:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )

    session.commit()
    session.refresh(sale)
    return sale

# End Sale Routes


# SALESDETAIL ROUTES
@app.post("/salesdetails", response_model=SalesDetailResponse)
def create_sales_detail(sd: SalesDetailRequest):
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


@app.get("/salesdetails/{detail_id}", response_model=SalesDetailResponse)
def get_single_sales_detail(detail_id):
    query = select(SalesDetail).where(SalesDetail.id == detail_id)
    detail = session.scalars(query).first()
    if detail is None:
        raise HTTPException(status_code=404, detail="Sales detail not found")
    return detail


@app.put("/salesdetails/{detail_id}", response_model=SalesDetailResponse)
def update_sales_detail(detail_id: int, sd: SalesDetailRequest):
    
    query = select(SalesDetail).where(SalesDetail.id == detail_id)
    detail = session.scalars(query).first()
    if detail is None:         
        raise HTTPException(
            status_code=404, 
            detail="Sales detail not found"
        )

    detail.product_id = sd.product_id
    detail.sale_id = sd.sale_id
    detail.quantity = sd.quantity

    session.commit()
    session.refresh(detail)
    return detail

# End SalesDetail Routes


# PAYMENT ROUTES
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


@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_single_payment(payment_id):
    query = select(Payment).where(Payment.id == payment_id)
    payment = session.scalars(query).first()
    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )
    return payment


@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id : int, pay : PaymentRequest):
    query = select(Payment).where(Payment.id == payment_id)
    payment = session.scalars(query).first()

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    payment.sale_id = pay.sale_id
    payment.amount_paid = pay.amount_paid
    payment.transaction_code = pay.transaction_code
    payment.mrid = pay.mrid
    payment.crid = pay.crid
    payment.status = pay.status
    payment.phone_number = pay.phone_number

    session.commit()
    session.refresh(payment)
    return payment


# End Payments Routes   

