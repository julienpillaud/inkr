from sqlalchemy.orm import Session

from app.models import Material, MaterialSku
from tests.fixtures.factories.base import AbstractFactory
from tests.fixtures.factories.material import MaterialFactory


class MaterialSkuFactory(AbstractFactory):
    def __init__(self, session: Session, material_factory: MaterialFactory):
        super().__init__(session)
        self.material_factory = material_factory

    def create_one(self, material: Material | None = None) -> MaterialSku:
        if material is None:
            material = self.material_factory.create_one()

        sku = MaterialSku(
            material_id=material.id,
            cerm_id=self.faker.text(),
            serial_number=self.faker.uuid4(),
            quantity_in_stock=self.faker.random_int(),
        )
        self.session.add(sku)
        self.session.commit()
        return sku

    def create_many(
        self, number: int, material: Material | None = None
    ) -> list[MaterialSku]:
        return [self.create_one(material=material) for _ in range(number)]
