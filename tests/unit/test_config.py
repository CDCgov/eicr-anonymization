import pytest

from eicr_anonymization.config import CustomConfig, DefaultConfig, Sensitivity


class TestCustomConfig:
    def test_iter(self):
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

        with pytest.raises(ValueError, match="Unknown type in configuration: UnknownType"):
            CustomConfig(test_config)

    def test_check_elements_unknown_attribute(self):
        """Test that the configuration checks for unknown attributes."""
        test_config = {
            "ClinicalDocument": {
                "attributes": {
                    "unknownAttribute": None
                },
            }
        }

        with pytest.raises(ValueError, match="Unknown attribute 'unknownAttribute' in type 'ClinicalDocument'"):
            CustomConfig(test_config)

    def test_check_elements_unknown_element(self):
        """Test that the configuration checks for unknown types, attributes, and elements."""
        test_config = {
            "ClinicalDocument": {
                "elements": {
                    "unknownElement": None
                },
            }
        }

        with pytest.raises(ValueError, match="Unknown element 'unknownElement' in type 'ClinicalDocument'"):
            CustomConfig(test_config)


class TestDefaultConfig:
    def test_check_elements_missing_type(self):
        """Test that the default configuration is loaded correctly."""
        test_config = {
            "ClinicalDocument": {
                "elements": {
                    "effectiveTime": None,
                },
            }
        }

        with pytest.raises(ValueError):
            DefaultConfig(test_config)

    def test_check_elements_unknown_type(self):
        pass

    def test_check_elements_unknown_attribute(self):
        pass

    def test_check_elements_unknown_element(self):
        pass