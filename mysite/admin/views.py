from sqladmin import ModelView
from mysite.database.models import User, Product, Order


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
        User.registered_date,
    ]


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id,
        Product.product_name,
        Product.price,
        Product.created_date,
    ]


class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.user_id,
        Order.product_id,
        Order.quantity,
        Order.total_price,
        Order.order_status,
    ]