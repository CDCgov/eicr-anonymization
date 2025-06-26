"""Unit tests for the configuration validation."""

import pytest
import yaml

from eicr_anonymization.config import (
    CustomConfig,
    DefaultConfig,
    MissingItem,
    Sensitivity,
    UnknownItem,
)


class TestCustomConfig:
    """Test the custom configuration validation."""

    def test_iter(self):
        """Test that the configuration can be iterated over."""
        test_config = {
            "ClinicalDocument": {
                "elements": {
                    "effectiveTime": "SAFE",
                }
            }
        }

        config = CustomConfig(test_config)
        assert isinstance(config, CustomConfig)
        first_item = next(iter(config))
        assert first_item == "ClinicalDocument"

    def test_getitem(self):
        """Test that the configuration can be accessed by key."""
        test_config = {
            "ClinicalDocument": {
                "elements": {
                    "effectiveTime": "SAFE",
                }
            }
        }
        config = CustomConfig(test_config)
        clinical_document_elements = config["ClinicalDocument"].elements

        assert clinical_document_elements == {"effectiveTime": Sensitivity.SAFE}

    def test_check_elements_unknown_type(self):
        """Test that the configuration checks for unknown types."""
        test_config = {
            "UnknownType": {
                "elements": {
                    "effectiveTime": None,
                }
            }
        }

        with pytest.raises(UnknownItem):
            CustomConfig(test_config)

    def test_check_elements_unknown_attribute(self):
        """Test that the configuration checks for unknown attributes."""
        test_config = {
            "ClinicalDocument": {
                "attributes": {"unknownAttribute": None},
            }
        }

        with pytest.raises(UnknownItem):
            CustomConfig(test_config)

    def test_check_elements_unknown_element(self):
        """Test that the configuration checks for unknown types, attributes, and elements."""
        test_config = {
            "ClinicalDocument": {
                "elements": {"unknownElement": None},
            }
        }

        with pytest.raises(UnknownItem):
            CustomConfig(test_config)


class TestDefaultConfig:
    """Test the default configuration validation."""

    def test_good_default(self):
        """Test that the default configuration is loaded correctly."""
        with open("src/eicr_anonymization/configs/default.yaml") as config_file:
            default_config = yaml.safe_load(config_file)
        validated_config = DefaultConfig(default_config)
        assert isinstance(validated_config, DefaultConfig)

    def test_check_elements_unknown_type(self):
        """Test that validation for the default config fails on unknown types."""
        with open("tests/test_data/configs/test_configs/default_with_unknown.yaml") as config_file:
            default_config = yaml.safe_load(config_file)
        with pytest.raises(UnknownItem):
            _ = DefaultConfig(default_config)

    def test_check_elements_missing_type(self):
        """Test that the default configuration is loaded correctly."""
        test_config = {
            "ClinicalDocument": {
                "elements": {
                    "effectiveTime": None,
                },
            }
        }

        with pytest.raises(MissingItem):
            DefaultConfig(test_config)
