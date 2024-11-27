import datetime
import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.entities import (
    MaterialStatus,
    MixtureStatus,
    RecipeStatus,
    RecipeVersionStatus,
)


class Base(DeclarativeBase):
    pass


class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


class Composition(Base, UUIDMixin):
    __tablename__ = "composition"

    recipe_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("recipe_version.id")
    )
    material_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("material.id"))
    quantity: Mapped[int]

    __table_args__ = (
        UniqueConstraint(
            "material_id", "recipe_version_id", name="index_material_recipe_version"
        ),
    )


class Material(Base, UUIDMixin):
    __tablename__ = "material"

    cerm_id: Mapped[str] = mapped_column(unique=True)
    code: Mapped[str] = mapped_column(unique=True)
    label: Mapped[str]
    status: Mapped[MaterialStatus]
    last_delivery_date: Mapped[datetime.datetime | None]


class MaterialSku(Base, UUIDMixin):
    __tablename__ = "material_sku"

    material_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("material.id"))
    cerm_id: Mapped[str] = mapped_column(unique=True)
    serial_number: Mapped[str]
    quantity_in_stock: Mapped[int]


class Mixture(Base, UUIDMixin):
    __tablename__ = "mixture"

    recipe_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("recipe_version.id")
    )
    quantity: Mapped[int]
    from_mixture_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("mixture.id"))
    from_mixture_quantity: Mapped[int | None]
    residue_quantity: Mapped[int | None]
    status: Mapped[MixtureStatus]


class MixtureMaterial(Base, UUIDMixin):
    __tablename__ = "mixture_material"

    mixture_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mixture.id"))
    sku_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("material_sku.id"))
    serial_number: Mapped[str]


class MixtureOrder(Base, UUIDMixin):
    __tablename__ = "mixture_order"

    mixture_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mixture.id"))
    cerm_id: Mapped[str]

    __table_args__ = (
        UniqueConstraint("mixture_id", "cerm_id", name="index_mixture_order"),
    )


class Recipe(Base, UUIDMixin):
    __tablename__ = "recipe"

    code: Mapped[str] = mapped_column(unique=True)
    label: Mapped[str]
    status: Mapped[RecipeStatus]
    comment: Mapped[str | None]
    material_inconsistency: Mapped[bool]


class RecipeVersion(Base, UUIDMixin):
    __tablename__ = "recipe_version"

    recipe_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("recipe.id"))
    number: Mapped[int]
    comment: Mapped[str | None]
    status: Mapped[RecipeVersionStatus]
