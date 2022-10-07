import re
import peewee

from models.base import BaseModel
from models.order import Order
from core.exceptions import StructureError


class Accounting(BaseModel):
    id = peewee.AutoField()
    profit = peewee.DecimalField()
    description = peewee.CharField()
    order = peewee.ForeignKeyField(Order, field='id')

    def __init__(self, profit: int | float, description: str, order: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.profit = profit
        self.description = description
        self.order = order

        # if we are in registering new data then validate the fields
        if not kwargs.get('id'):
            Accounting.validation(self.__dict__['__data__'])

    @staticmethod
    def validation(data: dict) -> None:
        """Regex validator"""

        patterns = {
            'profit': r'(^\d{1,10}\.\d{1,5}$)|(^\d{1,10}$)',
            'description': r'^.{1,250}$',
            'order': r'^\d{1,10}$',
            'id': r'^\d{1,}$'
        }

        messages = [
            'max 10 digits and 5 decimal places',
            'max 250 chars',
            'max 10 digits',
            'auto filled'
        ]

        counter = 0
        for key, value in data.items():
            if not re.match(patterns[key], str(value)):
                raise StructureError(key, messages[counter])
            counter += 1
