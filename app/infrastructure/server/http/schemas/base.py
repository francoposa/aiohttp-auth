"""Base Serializer"""


from marshmallow import Schema, post_dump


class BaseSchema(Schema):
    """Base Serializer"""

    class Meta:
        """Meta data for BaseSchema."""

        record_type = None

    @post_dump
    def tag_record_type(self, data):
        """Adds record type field post-dump."""
        data["record_type"] = self.Meta.record_type
