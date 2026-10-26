from fastapi import FastAPI
import uvicorn

from mysite.database.schemas import AIOrderInputSchema, AIOrderOutputSchema
from mysite.chain.order_chain import order_chain

from mysite.api import user, product, order, ai
from mysite.database.db import Base, engine
from mysite.admin.setup import setup_admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Delivery Service')

app.include_router(user.user_router)
app.include_router(product.product_router)
app.include_router(order.order_router)
app.include_router(ai.ai_router)

setup_admin(app)


@app.post("/ai/order/", response_model=AIOrderOutputSchema)
async def create_ai_order(data: AIOrderInputSchema):
    result = order_chain.invoke({"text": data.text})
    return result


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)