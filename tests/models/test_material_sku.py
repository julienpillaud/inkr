import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import MaterialSku
from tests.fixtures.factories.material import MaterialFactory
from tests.fixtures.factories.material_sku import MaterialSkuFactory


def test_material_sku(
    session: Session, material_sku_factory: MaterialSkuFactory
) -> None:
    number = random.randint(1, 5)
    material_sku = material_sku_factory.create_one()
    material_sku_factory.create_many(number - 1)

    material_skus_db = session.scalars(select(MaterialSku)).all()
    assert len(material_skus_db) == number

    material_sku_db = session.scalars(
        select(MaterialSku).where(MaterialSku.id == material_sku.id)
    ).one()
    assert material_sku_db.material_id == material_sku.material_id
    assert material_sku_db.cerm_id == material_sku.cerm_id
    assert material_sku_db.serial_number == material_sku.serial_number
    assert material_sku_db.quantity_in_stock == material_sku.quantity_in_stock


def test_material_sku_with_material(
    session: Session,
    material_sku_factory: MaterialSkuFactory,
    material_factory: MaterialFactory,
) -> None:
    material = material_factory.create_one()
    material_sku = material_sku_factory.create_one(material=material)

    material_sku_db = session.scalars(
        select(MaterialSku).where(MaterialSku.id == material_sku.id)
    ).one()
    assert material_sku_db.material_id == material.id
