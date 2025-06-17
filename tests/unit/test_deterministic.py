"""Unit tests for the deterministic decorator in the Anonymizer class."""

import random

from lxml import etree

from eicr_anonymization.anonymizer import deterministic


class TestAnonymizer:
    """Test class for testing the decorator with a mock Anonymizer."""

    def __init__(self, seed=1, deterministic_functions=False):
        """Initialize the test class with an option for deterministic functions."""
        self.is_deterministic = deterministic_functions
        self.seed =seed

    @deterministic
    def random_method(self, param1, param2="default"):
        """Return a random integer between 1 and 1000."""
        return random.randint(1, 1000)


class TestDeterministicDecorator:
    """Test suite for the deterministic_random decorator."""

    def test_decorator_with_deterministic_true(self):
        """Test that decorator makes methods deterministic when is_deterministic=True."""
        # Arrange
        obj = TestAnonymizer(deterministic_functions=True)

        # Act
        result1 = obj.random_method("test", "value")
        result2 = obj.random_method("test", "value")

        # Assert
        assert result1 == result2, "Same parameters should produce same results"

    def test_decorator_with_deterministic_false(self):
        """Test that decorator doesn't affect randomness when is_deterministic=False."""
        # Arrange
        obj = TestAnonymizer()  # No seed, so is_deterministic=False

        # Act - run multiple times to increase chance of different results
        results = [obj.random_method("test", "value") for _ in range(10)]

        # Assert - we expect some variation (not all results the same)
        # Note: There's a tiny chance all results are the same by coincidence
        assert len(set(results)) > 1, "Non-deterministic should produce varied results"

    def test_different_parameters_produce_different_results(self):
        """Test that different parameters produce different deterministic results."""
        # Arrange
        obj = TestAnonymizer(deterministic_functions=True)

        # Act
        result1 = obj.random_method("param1", "value1")
        result2 = obj.random_method("param1", "value2")  # Different param2
        result3 = obj.random_method("param2", "value1")  # Different param1

        # Assert
        assert result1 != result2, "Different param2 should produce different results"
        assert result1 != result3, "Different param1 should produce different results"
        assert result2 != result3, "All different parameters should produce different results"

    def test_default_parameters_consistency(self):
        """Test that default parameters are handled consistently."""
        # Arrange
        obj = TestAnonymizer(deterministic_functions=True)

        # Act
        result1 = obj.random_method("test")  # Using default param2
        result2 = obj.random_method("test", "default")  # Explicit default param2

        # Assert
        assert result1 == result2, "Default and explicit default parameters should be equivalent"

    def test_element_parameter(self):
        """Test that using an element as a parameter produces consistent results."""
        # Arrange
        obj = TestAnonymizer(deterministic_functions=True)
        xml = '<a attrA="test"><b attrI="test" attrJ="test2"/></a>'
        root = etree.fromstring(xml)
        etree.tostring(root)

        element = root.find(".//{test}b")

        # Act
        result1 = obj.random_method(element)
        result2 = obj.random_method(element)

        # Assert
        assert result1 == result2, "Same element parameter should produce same results"

    def test_with_different_seeds(self):
        """Test that different seeds will produce different results for the same parameters."""
        # Arrange
        obj_1 = TestAnonymizer(seed=1, deterministic_functions=True)
        obj_2 = TestAnonymizer(seed=2, deterministic_functions=True)

        # Act
        result1 = obj_1.random_method("test", "value")
        result2 = obj_2.random_method("test", "value")

        # Assert
        assert result1 != result2, "Same parameters should produce same results"
