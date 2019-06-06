from datetime import datetime

import attr
from attr.validators import instance_of, optional

from app.usecases.resources.utils import generate_uuid


@attr.s(slots=True)
class Role:

    role = attr.ib(validator=instance_of(str))
    permissions = attr.ib(validator=instance_of(list))

    # Auto-generated on creation of usecase object
    id = attr.ib(validator=instance_of(str), default=attr.Factory(generate_uuid))

    # DB auto created
    # When we create the usecase objects in the app or from a POST, these will not be set,
    # but when we create the objects by reading from the database, these will be set
    created_at = attr.ib(validator=optional(instance_of(datetime)), default=None)
    updated_at = attr.ib(validator=optional(instance_of(datetime)), default=None)
    enabled = attr.ib(validator=optional(instance_of(bool)), default=True)
