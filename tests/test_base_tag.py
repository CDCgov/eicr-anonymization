"""Test the Tag class."""

import pytest

from eicr_anonymization.tags.Tag import FamilyTag, Tag


def test_immutable_name():
    """Test that the name of the tag is immutable."""
    tag = FamilyTag()
    with pytest.raises(AttributeError):
        tag.name = "new_name"


def test_immutable_attributes():
    """Test that the attributes of the tag are immutable."""
    tag = FamilyTag()
    with pytest.raises(AttributeError):
        tag.sensitive_attr = "new_value"


def test_immutable_replacement_values():
    """Test that the replacement values of the tag are immutable."""
    tag = FamilyTag()
    with pytest.raises(AttributeError):
        tag.replacement_values = "new_value"


def test_get_registry():
    """Test the get_registry method."""
    registry = Tag.get_registry()
    assert registry["family"] == FamilyTag


