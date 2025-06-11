import random

from lxml import etree

from eicr_anonymization.anonymizer import deterministic
from eicr_anonymization.element_parser import Element


class TestAnonymizer:
    """Test class for testing the decorator with a mock Anonymizer."""

    def __init__(self, reproducible=False, deterministic_functions=False):
        if reproducible:
            random.seed(1701)  # Set a fixed seed for reproducibility
        self.is_deterministic = deterministic_functions

    @deterministic
    def random_method(self, param1, param2="default"):
        """Return a random integer between 1 and 1000."""
        return random.randint(1, 1000)


class TestDeterministicRandomDecorator:
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


    def test_determinism(self):
        """Test that the anonymizer's deterministic functions produce consistent results."""
        # Arrange
        anonymizer_1 = TestAnonymizer(deterministic_functions=True)
        anonymizer_2 = TestAnonymizer(deterministic_functions=True)

        id_element_1 = Element(
            etree.Element(
                "{urn:hl7-org:v3}id", attrib={"root": "test.id.123", "extension": "1234567890"}
            ),
            "II",
        )

        id_element_2 = Element(
            etree.Element(
                "{urn:hl7-org:v3}id", attrib={"root": "different.test.id.987", "extension": "011235813"}
            ),
            "II",
        )

        # Act
        id_result_1_1 = anonymizer_1.random_method(id_element_1)
        id_result_2_1 = anonymizer_1.random_method(id_element_2)

        id_result_2_2 = anonymizer_2.random_method(id_element_2)
        id_result_1_2 = anonymizer_2.random_method(id_element_1)

        # Assert
        assert id_result_1_1 == id_result_1_2, (
            "Anonymizer 1 and 2 should produce the same result for the same input"
        )
        assert id_result_2_1 == id_result_2_2, (
            "Anonymizer 1 and 2 should produce the same result for the same input"
        )

        assert id_result_1_1 != id_result_2_1, (
            "Anonymizer 1 and 2 should produce different results for different inputs"
        )
        assert id_result_1_2 != id_result_2_2, (
            "Anonymizer 1 and 2 should produce different results for different inputs"
        )


    def test_nondeterminism(self):
        """Test that the anonymizer's deterministic functions produce consistent results."""
        # Arrange
        anonymizer_1 = TestAnonymizer(reproducible=True)
        anonymizer_2 = TestAnonymizer(reproducible=True)

        id_element_1 = Element(
            etree.Element(
                "{urn:hl7-org:v3}id", attrib={"root": "test.id.123", "extension": "1234567890"}
            ),
            "II",
        )

        id_element_2 = Element(
            etree.Element(
                "{urn:hl7-org:v3}id", attrib={"root": "different.test.id.987", "extension": "011235813"}
            ),
            "II",
        )

        # Act
        id_result_1_1 = anonymizer_1.random_method(id_element_1)
        id_result_2_1 = anonymizer_1.random_method(id_element_2)

        id_result_2_2 = anonymizer_2.random_method(id_element_2)
        id_result_1_2 = anonymizer_2.random_method(id_element_1)

        # Assert
        assert id_result_1_1 != id_result_1_2, (
            "Anonymizer 1 and 2 should produce different results for the same input"
        )
        assert id_result_2_1 != id_result_2_2, (
            "Anonymizer 1 and 2 should produce different results for the same input"
        )

        assert id_result_1_1 != id_result_2_1, (
            "The Anonymizer should produce different results for different inputs"
        )
        assert id_result_1_2 != id_result_2_2, (
            "The Anonymizer should produce different results for different inputs"
        )
