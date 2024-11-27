import pytest
from sqlalchemy.orm import Session

from tests.fixtures.factories.composition import CompositionFactory
from tests.fixtures.factories.material import MaterialFactory
from tests.fixtures.factories.material_sku import MaterialSkuFactory
from tests.fixtures.factories.mixture import MixtureFactory
from tests.fixtures.factories.mixture_material import MixtureMaterialFactory
from tests.fixtures.factories.mixture_order import MixtureOrderFactory
from tests.fixtures.factories.recipe import RecipeFactory
from tests.fixtures.factories.recipe_version import RecipeVersionFactory


@pytest.fixture
def composition_factory(
    session: Session,
    recipe_version_factory: RecipeVersionFactory,
    material_factory: MaterialFactory,
) -> CompositionFactory:
    return CompositionFactory(
        session=session,
        recipe_version_factory=recipe_version_factory,
        material_factory=material_factory,
    )


@pytest.fixture
def material_factory(session: Session) -> MaterialFactory:
    return MaterialFactory(session=session)


@pytest.fixture
def material_sku_factory(
    session: Session, material_factory: MaterialFactory
) -> MaterialSkuFactory:
    return MaterialSkuFactory(session=session, material_factory=material_factory)


@pytest.fixture
def mixture_factory(
    session: Session, recipe_version_factory: RecipeVersionFactory
) -> MixtureFactory:
    return MixtureFactory(
        session=session, recipe_version_factory=recipe_version_factory
    )


@pytest.fixture
def mixture_material_factory(
    session: Session,
    material_sku_factory: MaterialSkuFactory,
    mixture_factory: MixtureFactory,
) -> MixtureMaterialFactory:
    return MixtureMaterialFactory(
        session=session,
        material_sku_factory=material_sku_factory,
        mixture_factory=mixture_factory,
    )


@pytest.fixture
def mixture_order_factory(
    session: Session, mixture_factory: MixtureFactory
) -> MixtureOrderFactory:
    return MixtureOrderFactory(session=session, mixture_factory=mixture_factory)


@pytest.fixture
def recipe_factory(session: Session) -> RecipeFactory:
    return RecipeFactory(session=session)


@pytest.fixture
def recipe_version_factory(
    session: Session, recipe_factory: RecipeFactory
) -> RecipeVersionFactory:
    return RecipeVersionFactory(session=session, recipe_factory=recipe_factory)
