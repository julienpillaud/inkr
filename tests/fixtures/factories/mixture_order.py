from sqlalchemy.orm import Session

from app.models import Mixture, MixtureOrder
from tests.fixtures.factories.base import AbstractFactory
from tests.fixtures.factories.mixture import MixtureFactory


class MixtureOrderFactory(AbstractFactory):
    def __init__(self, session: Session, mixture_factory: MixtureFactory):
        super().__init__(session=session)
        self.mixture_factory = mixture_factory

    def create_one(
        self, mixture: Mixture | None = None, cerm_id: str | None = None
    ) -> MixtureOrder:
        if mixture is None:
            mixture = self.mixture_factory.create_one()

        order = MixtureOrder(
            mixture_id=mixture.id,
            cerm_id=cerm_id if cerm_id is not None else self.faker.text(),
        )
        self.session.add(order)
        self.session.commit()
        return order

    def create_many(
        self,
        number: int,
        mixture: Mixture | None = None,
        cerm_id: str | None = None,
    ) -> list[MixtureOrder]:
        return [
            self.create_one(mixture=mixture, cerm_id=cerm_id) for _ in range(number)
        ]
