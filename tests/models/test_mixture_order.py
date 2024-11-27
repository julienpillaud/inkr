import random

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import MixtureOrder
from tests.fixtures.factories.mixture import MixtureFactory
from tests.fixtures.factories.mixture_order import MixtureOrderFactory


def test_mixture_order(
    session: Session, mixture_order_factory: MixtureOrderFactory
) -> None:
    number = random.randint(1, 5)
    mixture_order = mixture_order_factory.create_one()
    mixture_order_factory.create_many(number - 1)

    mixture_orders_db = session.scalars(select(MixtureOrder)).all()
    assert len(mixture_orders_db) == number

    mixture_order_db = session.scalars(
        select(MixtureOrder).where(MixtureOrder.id == mixture_order.id)
    ).one()
    assert mixture_order_db.mixture_id == mixture_order.mixture_id
    assert mixture_order_db.cerm_id == mixture_order.cerm_id


def test_mixture_order_with_mixture(
    session: Session,
    mixture_order_factory: MixtureOrderFactory,
    mixture_factory: MixtureFactory,
) -> None:
    mixture = mixture_factory.create_one()
    mixture_order = mixture_order_factory.create_one(mixture=mixture)

    mixture_order_db = session.scalars(
        select(MixtureOrder).where(MixtureOrder.id == mixture_order.id)
    ).one()
    assert mixture_order_db.mixture_id == mixture.id


def test_mixture_order_unique_mixture_cerm(
    session: Session,
    mixture_order_factory: MixtureOrderFactory,
    mixture_factory: MixtureFactory,
) -> None:
    mixture = mixture_factory.create_one()
    cerm_id = "test_cerm_id"

    mixture_order_factory.create_one(
        mixture=mixture,
        cerm_id=cerm_id,
    )

    with pytest.raises(IntegrityError, match="duplicate key.*index_mixture_order"):
        mixture_order_factory.create_one(
            mixture=mixture,
            cerm_id=cerm_id,
        )
