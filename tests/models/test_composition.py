import random

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Composition
from tests.fixtures.factories.composition import CompositionFactory
from tests.fixtures.factories.material import MaterialFactory
from tests.fixtures.factories.recipe_version import RecipeVersionFactory


def test_composition(session: Session, composition_factory: CompositionFactory) -> None:
    number = random.randint(1, 5)
    composition = composition_factory.create_one()
    composition_factory.create_many(number - 1)

    compositions_db = session.scalars(select(Composition)).all()
    assert len(compositions_db) == number

    composition_db = session.scalars(
        select(Composition).where(Composition.id == composition.id)
    ).one()
    assert composition_db.recipe_version_id == composition.recipe_version_id
    assert composition_db.material_id == composition.material_id
    assert composition_db.quantity == composition.quantity


def test_composition_with_material(
    session: Session,
    material_factory: MaterialFactory,
    composition_factory: CompositionFactory,
) -> None:
    material = material_factory.create_one()
    composition = composition_factory.create_one(material=material)

    composition_db = session.scalars(
        select(Composition).where(Composition.id == composition.id)
    ).one()
    assert composition_db.material_id == material.id


def test_composition_with_recipe_version(
    session: Session,
    recipe_version_factory: RecipeVersionFactory,
    composition_factory: CompositionFactory,
) -> None:
    recipe_version = recipe_version_factory.create_one()
    composition = composition_factory.create_one(recipe_version=recipe_version)

    composition_db = session.scalars(
        select(Composition).where(Composition.id == composition.id)
    ).one()
    assert composition_db.recipe_version_id == recipe_version.id


def test_composition_unique_material_recipe_version(
    session: Session,
    composition_factory: CompositionFactory,
    material_factory: MaterialFactory,
    recipe_version_factory: RecipeVersionFactory,
) -> None:
    material = material_factory.create_one()
    recipe_version = recipe_version_factory.create_one()

    composition_factory.create_one(
        material=material,
        recipe_version=recipe_version,
    )

    with pytest.raises(
        IntegrityError, match="duplicate key.*index_material_recipe_version"
    ):
        composition_factory.create_one(
            material=material,
            recipe_version=recipe_version,
        )
