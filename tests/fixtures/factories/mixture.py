from typing import Optional

from sqlalchemy.orm import Session

from app.entities import MixtureStatus
from app.models import Mixture, RecipeVersion
from tests.fixtures.factories.base import AbstractFactory
from tests.fixtures.factories.recipe_version import RecipeVersionFactory


class MixtureFactory(AbstractFactory):
    def __init__(self, session: Session, recipe_version_factory: RecipeVersionFactory):
        super().__init__(session)
        self.recipe_version_factory = recipe_version_factory

    def create_one(
        self,
        recipe_version: RecipeVersion | None = None,
        from_mixture: Optional["Mixture"] = None,
    ) -> Mixture:
        if recipe_version is None:
            recipe_version = self.recipe_version_factory.create_one()

        mixture = Mixture(
            recipe_version_id=recipe_version.id,
            quantity=self.faker.random_int(),
            from_mixture_id=from_mixture.id if from_mixture else None,
            from_mixture_quantity=self.faker.random_int() if from_mixture else None,
            residue_quantity=self.faker.random_int() if self.faker.boolean() else None,
            status=self.faker.random_element(MixtureStatus),
        )
        self.session.add(mixture)
        self.session.commit()
        return mixture

    def create_many(
        self,
        number: int,
        recipe_version: RecipeVersion | None = None,
        from_mixture: Optional["Mixture"] = None,
    ) -> list[Mixture]:
        return [
            self.create_one(recipe_version=recipe_version, from_mixture=from_mixture)
            for _ in range(number)
        ]
