from app.entities import RecipeStatus
from app.models import Recipe
from tests.fixtures.factories.base import AbstractFactory


class RecipeFactory(AbstractFactory):
    def create_one(self) -> Recipe:
        recipe = Recipe(
            code=self.faker.text(),
            label=self.faker.text(),
            status=self.faker.random_element(RecipeStatus),
            comment=self.faker.text() if self.faker.boolean() else None,
            material_inconsistency=self.faker.boolean(),
        )
        self.session.add(recipe)
        self.session.commit()
        return recipe

    def create_many(self, number: int, /) -> list[Recipe]:
        return [self.create_one() for _ in range(number)]
