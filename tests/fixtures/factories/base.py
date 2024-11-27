from faker import Faker
from sqlalchemy.orm import Session


class AbstractFactory:
    faker = Faker()

    def __init__(self, session: Session):
        self.session = session
