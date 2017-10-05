import datetime
import uuid

import pytest

from declaration import fields, models


class TestFields(object):

    def test_base_not_implemented(self):
        field = fields.DeclarativeField()

        with pytest.raises(NotImplementedError):
            field.parse("any value")

        with pytest.raises(NotImplementedError):
            field.encode("any value")

    def test_generic_is_a_passthrough(self):
        field = fields.GenericField()

        assert "exact value" == field.parse("exact value")
        assert "exact value" == field.encode("exact value")

    def test_string_field_converts(self):
        field = fields.StringField()

        assert "basic string" == field.parse("basic string")
        assert "basic string" == field.encode("basic string")
        assert "123" == field.parse(123)
        assert "123" == field.encode(123)

    def test_json_field_converts(self):
        field = fields.JSONField()

        assert {"value": "here"} == field.parse('{"value": "here"}')
        assert '{"value": "here"}' == field.encode({"value": "here"})
        assert None is field.parse(None)
        assert None is field.encode(None)

    def test_date_time_field_creates_proper_format(self):
        field = fields.DateTimeField()

        date_value = datetime.datetime(2010, 1, 1, 13, 23, 57)
        assert "2010-01-01T13:23:57Z" == field.encode(date_value)

    def test_date_time_field_recognizes_string_values(self):
        field = fields.DateTimeField()

        response = field.parse("2010-01-01T13:23:57Z").replace(tzinfo=None)
        assert datetime.datetime(2010, 1, 1, 13, 23, 57, ) == response

    def test_date_field_trims_excess_from_date_time(self):
        field = fields.DateField()

        date_value = datetime.datetime(2013, 7, 31, 1, 33, 10)
        assert date_value.date() == field.parse(date_value)

    def test_date_field_recognizes_string_values(self):
        field = fields.DateField()

        response = field.parse("2010-01-01T13:23:57Z")
        assert datetime.date(2010, 1, 1) == response

    def test_time_field_trims_excess_from_date_time(self):
        field = fields.TimeField()

        date_value = datetime.datetime(2013, 7, 31, 1, 33, 10)
        assert date_value.time() == field.parse(date_value)

    def test_date_time_fields_ignore_missing_values(self):
        field = fields.DateTimeField()
        assert field.parse("") == ""
        assert field.parse(None) is None
        assert field.encode("") == ""
        assert field.encode(None) is None

        field = fields.DateField()
        assert field.parse("") == ""
        assert field.parse(None) is None
        assert field.encode("") == ""
        assert field.encode(None) is None

        field = fields.TimeField()
        assert field.parse("") == ""
        assert field.parse(None) is None
        assert field.encode("") == ""
        assert field.encode(None) is None

    def test_uuid_field_converts(self):
        field = fields.UUIDField()
        value = "c3864285-1f1e-4c0c-bd95-ad5a8dbf3232"
        converted = uuid.UUID(value, version=4)

        assert converted == field.parse(value)

    def test_uuid_field_passes_through_if_already_uuid(self):
        field = fields.UUIDField()
        value = uuid.UUID("c3864285-1f1e-4c0c-bd95-ad5a8dbf3232", version=4)

        assert value == field.parse(value)

    def test_uuid_field_fails_if_not_uuid(self):
        field = fields.UUIDField()
        value = "garbage"

        assert "garbage" == field.parse(value)
        assert "garbage" == field.encode(value)

    def test_uuid_field_encodes_as_string(self):
        field = fields.UUIDField()
        value = "c3864285-1f1e-4c0c-bd95-ad5a8dbf3232"
        converted = uuid.UUID(value, version=4)

        assert value == field.encode(converted)

    def test_nested_field_parses(self):
        class NestedExample(models.DeclarativeBase):
            subtitle = fields.StringField()

        class Example(models.DeclarativeBase):
            title = fields.StringField()
            inner = fields.NestedField(NestedExample)

        nested = NestedExample()
        nested.subtitle = "Inner Text"

        example = Example()
        example.title = "Outer Text"
        example.inner = nested

        assert example.inner == nested
        assert example.inner.subtitle == "Inner Text"
