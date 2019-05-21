from typing import Mapping

import attr
from marshmallow import Schema, ValidationError


class BaseJSONUsecaseAdapter:
    """Class to marshal JSON into attrs classes using marshmallow"""

    def __init__(self, usecase_cls, schema: Schema):
        self.UsecaseClass = usecase_cls  # attrs class
        self.schema: Schema = schema

    def dict_to_usecase(self, mapping):
        """Return a UsecaseClass() from an HTTP Request."""

        try:
            usecase_data: Mapping = self.schema.load(mapping)
            return self.UsecaseClass(**usecase_data)
        except ValidationError as e:
            # TODO see what this error looks like, get useful info out, and re-raise as as a different error
            raise (e)

    def usecase_to_dict(self, usecase):
        return self.schema.dump(usecase)
