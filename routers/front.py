from typing import Annotated
from datetime import datetime, timedelta
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import HTMLResponse

from schemas.beens import SBeenAdd
from backend.repository import BeenRepository

router = APIRouter(prefix='', tags=['Front'])
templates = Jinja2Templates(directory='templates')


@router.get('/')
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {
        "request": request
    })


@router.get('/{hash}')
async def get_been_at_hash(request: Request, hash: str) -> HTMLResponse:
    been = await BeenRepository.get_at_hash(hash)
    if not been:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Been with a hash {hash} not found.'
        )

    if been.expire and been.expire < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='This been is expire!'
        )

    if been.delete_it:
        await BeenRepository.delete_at_hash(hash)

    return templates.TemplateResponse("index.html", {
        "request": request, "been": been
    })


@router.post('/')
async def add_been(request: Request, text: str = Form(),
                   days: int = Form(), minutes: int = Form(),
                   delete_it: Annotated[bool, Form()] = False) -> HTMLResponse:
    expire_date = datetime.now() + timedelta(days=days, minutes=minutes)

    new_been = SBeenAdd(
        text=text,
        expire=expire_date,
        delete_it=delete_it,
    )
    new_been = await BeenRepository.add(new_been)

    return templates.TemplateResponse("index.html", {
        "request": request, "been": new_been
    })
