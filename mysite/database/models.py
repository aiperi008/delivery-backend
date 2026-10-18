from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, DateTime, Text
from enum import Enum as PyEnum
from typing import List
from datetime import date, datetime


class OrderStatusChoices(str, PyEnum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    registered_date: Mapped[date] = mapped_column(Date, default=date.today)

    orders: Mapped[List['Order']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    orders: Mapped[List['Order']] = relationship(back_populates='product', cascade='all, delete-orphan')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    total_price: Mapped[int] = mapped_column(Integer)
    order_status: Mapped[OrderStatusChoices] = mapped_column(
        Enum(OrderStatusChoices),
        default=OrderStatusChoices.pending
    )
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(User, back_populates='orders')
    product: Mapped[Product] = relationship(Product, back_populates='orders')