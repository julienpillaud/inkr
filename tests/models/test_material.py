import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Material
from tests.fixtures.factories.material import MaterialFactory


def test_material(session: Session, material_factory: MaterialFactory) -> None:
    number = random.randint(1, 5)
    material = material_factory.create_one()
    material_factory.create_many(number - 1)

    materials_db = session.scalars(select(Material)).all()
    assert len(materials_db) == number

    material_db = session.scalars(
        select(Material).where(Material.id == material.id)
    ).one()
    assert material_db.cerm_id == material.cerm_id
    assert material_db.code == material.code
    assert material_db.label == material.label
    assert material_db.status == material.status
    assert material_db.last_delivery_date == material.last_delivery_date
