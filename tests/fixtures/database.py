from collections.abc import Iterator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.models import Base


@pytest.fixture(scope="session", autouse=True)
def engine() -> Iterator[Engine]:
    engine = create_engine(
        "postgresql+psycopg://pguser:test@localhost:1019/test",
    )

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    with Session(engine) as session:
        yield session

        session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())

        session.commit()
