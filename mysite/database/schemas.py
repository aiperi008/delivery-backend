from pydantic import BaseModel, EmailStr, Field
from .models import OrderStatusChoices
from datetime import date, datetime


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    registered_date: date


class UserInputSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class ProductOutSchema(BaseModel):
    id: int
    product_name: str
    price: int
    description: str
    created_date: datetime


class ProductInputSchema(BaseModel):
    product_name: str
    price: int
    description: str


class OrderOutSchema(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: int
    order_status: OrderStatusChoices
    created_date: datetime


class OrderInputSchema(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1
    total_price: int
    order_status: OrderStatusChoices = OrderStatusChoices.pending

class TicketInputSchema(BaseModel):
    text: str = Field(min_length=1, max_length=2000)

class TicketOutputSchema(BaseModel):
    answer: str = Field(min_length=1, max_length=300)
    order_id: int | None = Field(ge=1, default=None)
    priority: int = Field(ge=1, le=3)

class AnswerInputSchema(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    facts: str = Field(min_length=1, max_length=1000)

class AnswerOutputSchema(BaseModel):
    text_draft: str
    review: bool = True



class AIOrderInputSchema(BaseModel):
    text: str = Field(..., json_schema_extra={"example": "Салам! Хочу заказать свитер размером L"})


class AIOrderOutputSchema(BaseModel):
    title: str
    category: str
    price: int
    quantity: int
    total_price: int
    description: str

