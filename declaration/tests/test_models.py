import datetime
import json

from declaration import fields, models


class TestModels(object):

    def test_fields_added_to_class(self):
        class Example(models.DeclarativeBase):
            title = fields.StringField()

        example = Example()
        assert "title" in example._fields
        assert 1 == len(example._fields)

    def test_excludes_excess_fields(self):
        class Example(models.DeclarativeBase):
            only = fields.StringField()

        example = Example()
        example["something"] = "else"

        assert "only" in example._fields
        assert "something" not in example._fields
        assert 1 == len(example._fields)

    def test_get_raw_value_during_attribute_access(self):
        class Example(models.DeclarativeBase):
            timestamp = fields.DateTimeField()

        example = Example()
        example.timestamp = datetime.datetime(2010, 1, 1, 12, 0, 0)
        assert example.timestamp == datetime.datetime(2010, 1, 1, 12, 0, 0)

    def test_missing_attribute_returns_none(self):
        class Example(models.DeclarativeBase):
            anything = fields.StringField()

        example = Example()
        assert example.another is None

    def test_iterates_only_defined_fields(self):
        class Example(models.DeclarativeBase):
            only = fields.StringField()

        example = Example()
        example.only = "value"

        output = json.dumps(example)
        assert output == "{\"only\": \"value\"}"

    def test_json_dump_encodes_values(self):
        class Example(models.DeclarativeBase):
            timestamp = fields.DateTimeField()

        example = Example()
        example.timestamp = datetime.datetime(2010, 1, 1, 12, 0, 0)

        output = json.dumps(example)
        assert output == '{"timestamp": "2010-01-01T12:00:00"}'

    def test_get_attribute_stores_raw_value(self):
        class Example(models.DeclarativeBase):
            timestamp = fields.DateField()

        example = Example()
        example.timestamp = datetime.datetime(2010, 1, 1, 12, 0, 0)

        assert example.timestamp == datetime.date(2010, 1, 1)

    def test_get_as_dict_with_missing_key_returns_none(self):
        class Example(models.DeclarativeBase):
            anything = fields.StringField()

        example = Example()
        assert example["missing"] is None
