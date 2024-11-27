from sqlalchemy.orm import Session

from app.entities import RecipeVersionStatus
from app.models import Recipe, RecipeVersion
from tests.fixtures.factories.base import AbstractFactory
from tests.fixtures.factories.recipe import RecipeFactory


class RecipeVersionFactory(AbstractFactory):
    def __init__(self, session: Session, recipe_factory: RecipeFactory):
        super().__init__(session)
        self.recipe_factory = recipe_factory

    def create_one(self, recipe: Recipe | None = None) -> RecipeVersion:
        if recipe is None:
            recipe = self.recipe_factory.create_one()

        version = RecipeVersion(
            recipe_id=recipe.id,
            number=self.faker.random_int(),
            comment=self.faker.text() if self.faker.boolean() else None,
            status=self.faker.random_element(RecipeVersionStatus),
        )
        self.session.add(version)
        self.session.commit()
        return version

    def create_many(
        self, number: int, recipe: Recipe | None = None
    ) -> list[RecipeVersion]:
        return [self.create_one(recipe=recipe) for _ in range(number)]
