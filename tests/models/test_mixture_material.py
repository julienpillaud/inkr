import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import MixtureMaterial
from tests.fixtures.factories.material_sku import MaterialSkuFactory
from tests.fixtures.factories.mixture import MixtureFactory
from tests.fixtures.factories.mixture_material import MixtureMaterialFactory


def test_mixture_material(
    session: Session, mixture_material_factory: MixtureMaterialFactory
) -> None:
    number = random.randint(1, 5)
    mixture_material = mixture_material_factory.create_one()
    mixture_material_factory.create_many(number - 1)

    mixture_materials_db = session.scalars(select(MixtureMaterial)).all()
    assert len(mixture_materials_db) == number

    mixture_material_db = session.scalars(
        select(MixtureMaterial).where(MixtureMaterial.id == mixture_material.id)
    ).one()
    assert mixture_material_db.mixture_id == mixture_material.mixture_id
    assert mixture_material_db.sku_id == mixture_material.sku_id
    assert mixture_material_db.serial_number == mixture_material.serial_number


def test_mixture_material_with_mixture(
    session: Session,
    mixture_material_factory: MixtureMaterialFactory,
    mixture_factory: MixtureFactory,
) -> None:
    mixture = mixture_factory.create_one()
    mixture_material = mixture_material_factory.create_one(mixture=mixture)

    mixture_material_db = session.scalars(
        select(MixtureMaterial).where(MixtureMaterial.id == mixture_material.id)
    ).one()
    assert mixture_material_db.mixture_id == mixture.id


def test_mixture_material_with_material_sku(
    session: Session,
    mixture_material_factory: MixtureMaterialFactory,
    material_sku_factory: MaterialSkuFactory,
) -> None:
    material_sku = material_sku_factory.create_one()
    mixture_material = mixture_material_factory.create_one(material_sku=material_sku)

    mixture_material_db = session.scalars(
        select(MixtureMaterial).where(MixtureMaterial.id == mixture_material.id)
    ).one()
    assert mixture_material_db.sku_id == material_sku.id
