import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Mixture
from tests.fixtures.factories.mixture import MixtureFactory
from tests.fixtures.factories.recipe_version import RecipeVersionFactory


def test_mixture(session: Session, mixture_factory: MixtureFactory) -> None:
    number = random.randint(1, 5)
    mixture = mixture_factory.create_one()
    mixture_factory.create_many(number - 1)

    mixtures_db = session.scalars(select(Mixture)).all()
    assert len(mixtures_db) == number

    mixture_db = session.scalars(select(Mixture).where(Mixture.id == mixture.id)).one()
    assert mixture_db.recipe_version_id == mixture.recipe_version_id
    assert mixture_db.quantity == mixture.quantity
    assert mixture_db.from_mixture_id == mixture.from_mixture_id
    assert mixture_db.from_mixture_quantity == mixture.from_mixture_quantity
    assert mixture_db.residue_quantity == mixture.residue_quantity
    assert mixture_db.status == mixture.status


def test_mixture_with_recipe_version(
    session: Session,
    mixture_factory: MixtureFactory,
    recipe_version_factory: RecipeVersionFactory,
) -> None:
    recipe_version = recipe_version_factory.create_one()
    mixture = mixture_factory.create_one(recipe_version=recipe_version)

    mixture_db = session.scalars(select(Mixture).where(Mixture.id == mixture.id)).one()
    assert mixture_db.recipe_version_id == recipe_version.id


def test_mixture_with_from_mixture(
    session: Session,
    mixture_factory: MixtureFactory,
) -> None:
    parent_mixture = mixture_factory.create_one()
    child_mixture = mixture_factory.create_one(from_mixture=parent_mixture)

    mixture_db = session.scalars(
        select(Mixture).where(Mixture.id == child_mixture.id)
    ).one()
    assert mixture_db.from_mixture_id == parent_mixture.id
    assert mixture_db.from_mixture_quantity is not None
