import re
from peewee import *

from model.configs import db
from model.configs import BaseModel
from model.order import Order
from exceptions import StructureError


def create_tables():
    with db:
        db.create_tables([Receipts])


class Receipts(BaseModel):

    id = PrimaryKeyField()
    cost = DecimalField()
    delivery = TimestampField()
    code = IntegerField()
    customer = CharField()
    desk = IntegerField()
    order_id = ForeignKeyField(Order, to_field="id")

    def __init__(self, cost: int | float, delivery: str, code: int, customer: str, desk: int) -> None:
        super().__init__()
        self.cost = cost
        self.delivery = delivery
        self.code = code
        self.customer = customer
        self.desk = desk
        Receipts.validation(self.__dict__['__data__'])
        self.save(self)

    @staticmethod
    def validation(data: dict) -> None:
        """Regex validator"""

        patterns = {
            'cost': r'^[1-9]\d*(\.\d+)?$',
            'delivery': r'^.{1,50}$',
            'code': r'^\d{1,5}$',
            'customer': r'^([a-zA-Z]+[a-zA-Z\- ]*[a-zA-Z]+){2,50}$',
            'desk': r'^\d{1,3}$',
        }

        messages = [
            'integer or decimal number',
            'max 50 char',
            'numeric max 5 digits',
            'alphabetic 2~50 char',
            'numeric max 3 digits',
        ]

        counter = 0
        for key, value in data.items():
            if not re.match(patterns[key], str(value)):
                raise StructureError(key, messages[counter])
            counter += 1
