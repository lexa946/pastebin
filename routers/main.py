from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Form, Depends, HTTPException
from starlette import status

from schemas.beens import SBeenAdd, SBeen
from schemas.responses import SBeenResponse, SBeensResponse
from backend.repository import BeenRepository

router = APIRouter(prefix='/api/v1', tags=['Beens'])



@router.post('/')
async def add_been(been: Annotated[SBeenAdd, Depends()]) -> SBeenResponse:
    new_been = await BeenRepository.add(been)
    return {
        'status_code': status.HTTP_201_CREATED,
        'been': new_been
    }



@router.get('/')
async def get_all_beens() -> SBeensResponse:
    return {
        'status_code': status.HTTP_200_OK,
        'beens': await BeenRepository.get_all()
    }




@router.get('/{hash}')
async def get_at_hash(hash: str) -> SBeenResponse:
    been = await BeenRepository.get_at_hash(hash)
    if not been:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Been with a hash {hash} not found.'
        )

    if been.expire < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='This been is expire!'
        )

    return {
        'status_code': status.HTTP_200_OK,
        'been': been
    }