from fastapi import FastAPI
from sqlalchemy.orm import Session
from data_schemas import ProductRequest, ProductResponse
from models import Base, Product, User
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
    
add_user()


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