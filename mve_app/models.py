# Based on https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from mve_app.database import Base


class T1(Base):
    # Based on https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-core
    __tablename__ = "t1"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)
    character: Mapped[str] = mapped_column(String(50))
