import re
import peewee

from models.base import BaseModel
from core.exceptions import StructureError


class Ingredient(BaseModel):
    id = peewee.AutoField()
    name = peewee.CharField()
    unit = peewee.CharField()
    cost = peewee.DecimalField()

    def __init__(self, name: str,  unit: str, cost: int | float, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = name
        self.unit = unit
        self.cost = cost

        # if we are in registering new data then validate the fields
        if not kwargs.get('id'):
            Ingredient.validation(self.__dict__['__data__'])

    @staticmethod
    def validation(data: dict) -> None:
        """Regex validator"""

        patterns = {
            'name': r'^([a-zA-Z]+[a-zA-Z\- ]*[a-zA-Z]+){1,30}$',
            'unit': r'^.{1,40}$',
            'cost': r'(^\d{1,10}\.\d{1,5}$)|(^\d{1,10}$)',
            'id': r'^\d{1,}$'
        }

        messages = [
            'alphabetic 2~30 char',
            'max 40 chars',
            'max 10 digits and 5 decimal places',
            'auto filled'
        ]

        counter = 0
        for key, value in data.items():
            if not re.match(patterns[key], str(value)):
                raise StructureError(key, messages[counter])
            counter += 1
