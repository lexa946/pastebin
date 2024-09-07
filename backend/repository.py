from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.beens import SBeenAdd, SBeen
from backend.db import new_session
from models.beens import BeenOrm

from uuid import uuid4


class BeenRepository:

    @classmethod
    async def add(cls, been: SBeenAdd) -> SBeen:
        async with new_session() as db:
            db: AsyncSession

            hash = str(uuid4())
            new_been = BeenOrm(**been.model_dump(), hash=hash)
            db.add(new_been)
            await db.flush()
            await db.commit()
            return SBeen.parse_obj(new_been)

    @classmethod
    async def get_all(cls) -> list[SBeen]:
        async with new_session() as db:
            db: AsyncSession

            query = await db.scalars(
                select(BeenOrm)
            )
            beens = query.all()
            return beens

    @classmethod
    async def get_at_hash(cls, hash: str) -> SBeen | None:
        async with new_session() as db:
            db: AsyncSession

            been = await db.scalar(
                select(BeenOrm).where(BeenOrm.hash == hash)
            )
            if not been:
                return None
            return been
