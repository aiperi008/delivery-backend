import asyncio

from fastapi import APIRouter, HTTPException
from langchain_core.exceptions import OutputParserException

from mysite.database.schemas import (
    TicketInputSchema,
    TicketOutputSchema,
    AnswerInputSchema,
    AnswerOutputSchema,
)
from mysite.chain.ticket_chain import ticket_chain, answer_chain
ai_router = APIRouter(prefix='/ai', tags=['AI Assistant'])

MODEL_TIMEOUT = 120


@ai_router.post('/analyze', response_model=TicketOutputSchema)
async def analyze_ticket(ticket: TicketInputSchema):
    text = ticket.text.strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилген')

    try:
        result = await asyncio.wait_for(
            ticket_chain.ainvoke({"text": text}),
            timeout=MODEL_TIMEOUT,
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail='Модель убагында жооп берген жок')
    except OutputParserException:
        raise HTTPException(status_code=422, detail='Моделдин жообу схемага туура келбейт')
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Моделге кошулууда ката: {e}')

    return result


@ai_router.post('/answer', response_model=AnswerOutputSchema)
async def answer_list(answer: AnswerInputSchema):
    text = answer.text.strip()
    facts = answer.facts.strip()

    if not text or not facts:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилген')

    try:
        result = await asyncio.wait_for(
            answer_chain.ainvoke({"text": text, "facts": facts}),
            timeout=MODEL_TIMEOUT,
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail='Модель убагында жооп берген жок')
    except OutputParserException:
        raise HTTPException(status_code=422, detail='Моделдин жообу схемага туура келбейт')
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Моделге кошулууда ката: {e}')

    return AnswerOutputSchema(text_draft=result)