from sqlalchemy.orm import Session

from app.models import MaterialSku, Mixture, MixtureMaterial
from tests.fixtures.factories.base import AbstractFactory
from tests.fixtures.factories.material_sku import MaterialSkuFactory
from tests.fixtures.factories.mixture import MixtureFactory


class MixtureMaterialFactory(AbstractFactory):
    def __init__(
        self,
        session: Session,
        mixture_factory: MixtureFactory,
        material_sku_factory: MaterialSkuFactory,
    ):
        super().__init__(session)
        self.mixture_factory = mixture_factory
        self.material_sku_factory = material_sku_factory

    def create_one(
        self, mixture: Mixture | None = None, material_sku: MaterialSku | None = None
    ) -> MixtureMaterial:
        if mixture is None:
            mixture = self.mixture_factory.create_one()
        if material_sku is None:
            material_sku = self.material_sku_factory.create_one()

        mixture_material = MixtureMaterial(
            mixture_id=mixture.id,
            sku_id=material_sku.id,
            serial_number=self.faker.uuid4(),
        )
        self.session.add(mixture_material)
        self.session.commit()
        return mixture_material

    def create_many(
        self,
        number: int,
        mixture: Mixture | None = None,
        material_sku: MaterialSku | None = None,
    ) -> list[MixtureMaterial]:
        return [
            self.create_one(mixture=mixture, material_sku=material_sku)
            for _ in range(number)
        ]
