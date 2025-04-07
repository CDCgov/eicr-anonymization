"""Test test_data_cache.py."""

import pytest
from eicr_anonymization.data_cache import NormalizedTagGroups
from eicr_anonymization.tags.Tag import FamilyTag


class TestDataCache:
    """Test the DataCache class."""

    def test_init(cls):
        """Test the initialization of the NormalizedTagGroups class."""
        data_cache = NormalizedTagGroups()
        assert len(data_cache) == 0

    def test_add(cls):
        """Test the add method of the NormalizedTagGroups class."""
        data_cache = NormalizedTagGroups()
        tag = FamilyTag("Bloggs")

        data_cache.add(tag)

        assert len(data_cache) == 1

    @pytest.mark.parametrize(
        ("tag1_string", "tag2_string", "expected_num"),
        [("Bloggs", "Smith", 2), ("Bloggs", "Bloggs", 1), ("Bloggs", "BLOGGS", 1)],
    )
    def test_add_multiple(cls, tag1_string, tag2_string, expected_num):
        """Test the add method of the NormalizedTagGroups class with multiple tags."""
        data_cache = NormalizedTagGroups()
        tag1 = FamilyTag(tag1_string)
        tag2 = FamilyTag(tag2_string)

        data_cache.add(tag1)
        data_cache.add(tag2)

        assert len(data_cache) == expected_num
