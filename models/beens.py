from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from backend.db import Base


class BeenOrm(Base):
    __tablename__ = 'beens'


    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str]
    hash: Mapped[str] = mapped_column(unique=True)
    expire: Mapped[datetime|None] = mapped_column(default=None)
    delete_it: Mapped[bool] = mapped_column(default=False)