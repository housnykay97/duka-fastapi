from fastapi import FastAPI
from sqlalchemy.orm import Session
from data_schemas import ProductRequest, ProductResponse
from models import Base, Product
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

@app.post("/products")
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
    return {"dbprod":dbprod}