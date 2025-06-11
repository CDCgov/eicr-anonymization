import random

from eicr_anonymization.anonimizer import deterministic


class TestAnonymizer:
    """Test class for testing the decorator with a mock Anonymizer."""

    def __init__(self, seed=None):
        self.is_deterministic = seed is not None
        if seed is not None:
            self.base_seed = seed

    @deterministic
    def random_method(self, param1, param2="default", param3=None):
        """Return a random integer between 1 and 1000."""
        return random.randint(1, 1000)


class TestDeterministicRandomDecorator:
    """Test suite for the deterministic_random decorator."""

    def test_decorator_with_deterministic_true(self):
        """Test that decorator makes methods deterministic when is_deterministic=True."""
        # Arrange
        obj = TestAnonymizer(seed=123)

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
        obj = TestAnonymizer(seed=123)

        # Act
        result1 = obj.random_method("param1", "value1")
        result2 = obj.random_method("param1", "value2")  # Different param2
        result3 = obj.random_method("param2", "value1")  # Different param1

        # Assert
        assert result1 != result2, "Different param2 should produce different results"
        assert result1 != result3, "Different param1 should produce different results"
        assert result2 != result3, "All different parameters should produce different results"
