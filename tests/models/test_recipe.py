import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Recipe
from tests.fixtures.factories.recipe import RecipeFactory


def test_recipe(session: Session, recipe_factory: RecipeFactory) -> None:
    number = random.randint(1, 5)
    recipe = recipe_factory.create_one()
    recipe_factory.create_many(number - 1)

    recipes_db = session.scalars(select(Recipe)).all()
    assert len(recipes_db) == number

    recipe_db = session.scalars(select(Recipe).where(Recipe.id == recipe.id)).one()
    assert recipe_db.code == recipe.code
    assert recipe_db.label == recipe.label
    assert recipe_db.status == recipe.status
    assert recipe_db.comment == recipe.comment
    assert recipe_db.material_inconsistency == recipe.material_inconsistency
