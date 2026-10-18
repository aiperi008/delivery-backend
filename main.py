from fastapi import FastAPI
import uvicorn

from mysite.api import user, product, order, ai
from mysite.database.db import Base, engine
from mysite.admin.setup import setup_admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Delivery Service')

app.include_router(user.user_router)
app.include_router(product.product_router)
app.include_router(order.order_router)
app.include_router(ai.ai_router)  # <-- Ушул сапты кошуңуз

setup_admin(app)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)