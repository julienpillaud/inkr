from app.entities import MaterialStatus
from app.models import Material
from tests.fixtures.factories.base import AbstractFactory


class MaterialFactory(AbstractFactory):
    def create_one(self) -> Material:
        material = Material(
            cerm_id=self.faker.text(),
            code=self.faker.text(),
            label=self.faker.text(),
            status=self.faker.random_element(MaterialStatus),
        )
        self.session.add(material)
        self.session.commit()
        return material

    def create_many(self, number: int, /) -> list[Material]:
        return [self.create_one() for _ in range(number)]
