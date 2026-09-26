from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


class CalculationHistory(Base):
    __tablename__ = "calculation_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    expression: Mapped[str] = mapped_column(String(255), nullable=False)
    result: Mapped[Decimal] = mapped_column(Numeric(20, 10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


def create_database(database_url: str):
    connect_args = (
        {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    )
    engine = create_engine(database_url, connect_args=connect_args)
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )
    return engine, session_factory


def get_db():
    settings = get_settings()
    _, session_factory = create_database(settings.database_url)
    with session_factory() as session:
        yield session
