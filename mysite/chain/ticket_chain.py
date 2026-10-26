from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from config import OLLAMA_URL, OLLAMA_MODEL
from mysite.database.schemas import TicketOutputSchema

llm = ChatOllama(
    base_url=OLLAMA_URL,
    model=OLLAMA_MODEL,
    temperature=0,
)


ticket_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Ты помощник службы поддержки службы доставки. "
            "Проанализируй обращение клиента и верни структурированный ответ. "
            "Определи приоритет обращения (например: low, medium, high) "
            "и подготовь краткий вежливый ответ клиенту. "
            "Отвечай на том же языке, на котором написано обращение.",
        ),
        ("human", "Обращение клиента: {text}"),
    ]
)


ticket_chain = ticket_prompt | llm.with_structured_output(TicketOutputSchema)



answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Ты оператор службы поддержки. Напиши вежливый ответ клиенту, "
            "используя ТОЛЬКО предоставленные факты. Ничего не выдумывай. "
            "Отвечай на том же языке, на котором написано обращение.",
        ),
        (
            "human",
            "Обращение клиента: {text}\n\nФакты: {facts}\n\nНапиши черновик ответа.",
        ),
    ]
)

answer_chain = answer_prompt | llm | StrOutputParser()