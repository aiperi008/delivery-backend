from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import ChatOllama
from config import OLLAMA_URL, OLLAMA_MODEL
from mysite.database.schemas import AIOrderOutputSchema


parser = JsonOutputParser(pydantic_object=AIOrderOutputSchema)

order_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Ты — AI-помощник магазина. Извлеки из сообщения клиента информацию о товаре и верни JSON. "
        "Поля: title (строка), category (строка), price (цена в виде целого числа, без букв и null), "
        "quantity (количество цифрой, например 1), total_price (общая сумма цифрой), "
        "description (краткое описание).\n"
        "ВАЖНО: Поля price, quantity и total_price ВСЕГДА должны быть числами (integer), а не пустыми!\n"
        "{format_instructions}"
    ),
    ("human", "{text}")
]).partial(format_instructions=parser.get_format_instructions())

model = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_URL, temperature=0)

order_chain = order_prompt | model | parser