from sqlalchemy.orm import Session

from app.models import Composition, Material, RecipeVersion
from tests.fixtures.factories.base import AbstractFactory
from tests.fixtures.factories.material import MaterialFactory
from tests.fixtures.factories.recipe_version import RecipeVersionFactory


class CompositionFactory(AbstractFactory):
    def __init__(
        self,
        session: Session,
        recipe_version_factory: RecipeVersionFactory,
        material_factory: MaterialFactory,
    ):
        super().__init__(session)
        self.recipe_version_factory = recipe_version_factory
        self.material_factory = material_factory

    def create_one(
        self,
        recipe_version: RecipeVersion | None = None,
        material: Material | None = None,
    ) -> Composition:
        if recipe_version is None:
            recipe_version = self.recipe_version_factory.create_one()
        if material is None:
            material = self.material_factory.create_one()

        composition = Composition(
            recipe_version_id=recipe_version.id,
            material_id=material.id,
            quantity=self.faker.random_int(),
        )
        self.session.add(composition)
        self.session.commit()
        return composition

    def create_many(
        self,
        number: int,
        recipe_version: RecipeVersion | None = None,
        material: Material | None = None,
    ) -> list[Composition]:
        return [
            self.create_one(recipe_version=recipe_version, material=material)
            for _ in range(number)
        ]
