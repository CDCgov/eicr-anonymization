"""Tests for the TimeTag class."""

from datetime import datetime

import pytest

from eicr_anonymization.tags.Tag import TimeTag


class TestTimeTag:
    """Test the TimeTag class."""

    def test_name(self):
        """Test the name property."""
        tag = TimeTag()
        assert tag.name == "time"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<time />"),
            ("test", None, "<time>test</time>"),
            (
                "test",
                {"test_attr": "test_value"},
                '<time test_attr="test_value">test</time>',
            ),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = TimeTag(text, attributes)
        assert repr(tag) == expected

    @pytest.mark.parametrize(
        ("orginal_values", "formats"),
        [
            (
                ("20080718025411+0000", "20080718"),
                ("%Y%m%d%H%M%S%z", "%Y%m%d"),
            ),
            (
                (
                    "20111020080547-0400",
                    "20250626",
                    "20111020",
                    "20190411224401-0400",
                    "20130104060902-0500",
                    "20221101110239+0000",
                ),
                (
                    "%Y%m%d%H%M%S%z",
                    "%Y%m%d",
                    "%Y%m%d",
                    "%Y%m%d%H%M%S%z",
                    "%Y%m%d%H%M%S%z",
                    "%Y%m%d%H%M%S%z",
                ),
            ),
            (
                ("20201107094421-0500", "20171001", "201710011035"),
                ("%Y%m%d%H%M%S%z", "%Y%m%d", "%Y%m%d%H%M"),
            ),
        ],
    )
    @pytest.mark.repeat(3)
    def test_get_replacement_mapping(self, set_random_seed, orginal_values, formats):
        """Test the get_replacement_mapping method."""
        tags = []
        replacements_dates = []
        for orginal_value, format in zip(orginal_values, formats, strict=False):
            tag = TimeTag(attributes={"value": orginal_value})
            tags.append(tag)
            replacement_mapping = TimeTag.get_replacement_mapping(tag, {tag})
            # Check that the value is the expected date format
            try:
                replacement_value = replacement_mapping[tag].attributes["value"]
                replacement_date = datetime.strptime(replacement_value, format)
                replacements_dates.append(replacement_date)
            except ValueError:
                pytest.fail(
                    f"Replacement value is not in the expected date format: Orginal value: {orginal_value} Replacement value: {replacement_value}"
                )
