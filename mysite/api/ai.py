import asyncio
from fastapi import APIRouter, HTTPException
from mysite.database.schemas import TicketInputSchema, TicketOutputSchema, AnswerInputSchema, AnswerOutputSchema
from langchain_core.exceptions import OutputParserException

ai_router = APIRouter(prefix='/ai', tags=['AI Assistant'])


@ai_router.post('/analyze', response_model=TicketOutputSchema)
async def analyze_ticke(ticket: TicketInputSchema):
    text = ticket.text.strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилген')

    try:
        result = {}
    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модель тапшырманы аткарганы текшерген жок')
    except OutputParserException:
        raise HTTPException(status_code=422, detail='Моделдин жообу схемага туура келбейт')

    return result


@ai_router.post('/answer', response_model=AnswerOutputSchema)
async def answer_list(answer: AnswerInputSchema):
    text = answer.text.strip()
    facts = answer.facts.strip()

    if not text or not facts:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилген')

    try:
        result = "Жооп текстин жазыңыз"
    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модель тапшырманы аткарганы текшерген жок')
    except OutputParserException:
        raise HTTPException(status_code=422, detail='Моделдин жообу схемага туура келбейт')

    return AnswerOutputSchema(text_draft=result)