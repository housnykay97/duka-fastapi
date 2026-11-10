from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declared_attr
from datetime import datetime, timezone
from sqlalchemy import DateTime

class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda:datetime.now())


class User(TimestampMixin, Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name : Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(100))
    phone_number : Mapped[str] = mapped_column(String(50))
    password : Mapped[str] = mapped_column(String(200))


class Product(TimestampMixin, Base):
    __tablename__ = "products"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_name: Mapped[str] = mapped_column(String(100))
    buying_price: Mapped[float] = mapped_column(Float)
    selling_price: Mapped[float] = mapped_column(Float)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)


class Purchase(TimestampMixin, Base):
    __tablename__ = "purchases"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id")) 
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    total_cost: Mapped[float] = mapped_column(Float)

    
class Sale(TimestampMixin, Base):
    __tablename__ = "sales"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    

class SalesDetail(Base):
    __tablename__ = "sales_details"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"))
    quantity: Mapped[int] = mapped_column(Integer)


class Payment(TimestampMixin, Base):
    __tablename__ = "payments"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"))
    amount_paid: Mapped[float] = mapped_column(Float)
    transaction_code: Mapped[str] = mapped_column(String, nullable=True, default=None)
    mrid: Mapped[str] = mapped_column(String)
    crid: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending")
    phone_number: Mapped[str] = mapped_column(String)
    # created_at: Mapped[datetime]



