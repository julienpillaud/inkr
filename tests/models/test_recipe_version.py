import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import RecipeVersion
from tests.fixtures.factories.recipe import RecipeFactory
from tests.fixtures.factories.recipe_version import RecipeVersionFactory


def test_recipe_version(
    session: Session, recipe_version_factory: RecipeVersionFactory
) -> None:
    number = random.randint(1, 5)
    recipe_version = recipe_version_factory.create_one()
    recipe_version_factory.create_many(number - 1)

    versions_db = session.scalars(select(RecipeVersion)).all()
    assert len(versions_db) == number

    version_db = session.scalars(
        select(RecipeVersion).where(RecipeVersion.id == recipe_version.id)
    ).one()
    assert version_db.recipe_id == recipe_version.recipe_id
    assert version_db.number == recipe_version.number
    assert version_db.comment == recipe_version.comment
    assert version_db.status == recipe_version.status


def test_recipe_version_with_recipe(
    session: Session,
    recipe_factory: RecipeFactory,
    recipe_version_factory: RecipeVersionFactory,
) -> None:
    recipe = recipe_factory.create_one()
    version = recipe_version_factory.create_one(recipe=recipe)

    version_db = session.scalars(
        select(RecipeVersion).where(RecipeVersion.id == version.id)
    ).one()
    assert version_db.recipe_id == recipe.id
