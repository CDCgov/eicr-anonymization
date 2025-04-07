import random

import pytest

from eicr_anonymization.tags.Tag import (
    CityTag,
    CountryTag,
    CountyTag,
    FamilyTag,
    GivenTag,
    HighTag,
    LowTag,
    NameTag,
    PostalCodeTag,
    PrefixTag,
    StateTag,
    StreetAddressLineTag,
    SuffixTag,
    TelecomTag,
    TimeTag,
)


@pytest.fixture
def set_random_seed(request):
    """Set up a random seed for reproducibility.

    This fixture ensures that the random seed is set to a fixed value for the first iteration of
    each test function. This ensures that we get deterministic results regardless of the order
    in which the tests are run.
    """
    callspec = getattr(request.node, "callspec", None)
    repeat_iteration = callspec.params.get("__pytest_repeat_step_number", 0) if callspec else 0
    random.seed(repeat_iteration)


class TestFamilyTag:
    """Test the FamilyTag class.

    This class does a lot of heavy lifting to test the base Tag class because it currently does not
    have any of it's own logic. Other simple tags can skip these tests.
    """

    def test_init(self):
        """Test the initialization of the FamilyTag class."""
        tag = FamilyTag()
        assert tag.text is None
        assert tag.attributes == {}

    def test_name(self):
        """Test the name property."""
        tag = FamilyTag()
        assert tag.name == "family"

    def test_text(self):
        """Test the text property."""
        tag = FamilyTag("Bloggs")
        assert tag.text == "Bloggs"

    def test_attributes(self):
        """Test the attributes property."""
        attributes = {"test_attr": "test_value"}
        tag = FamilyTag("testName", attributes)
        assert tag.attributes == attributes

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<family />"),
            ("test", None, "<family>test</family>"),
            ("test", {"test_attr": "test_value"}, '<family test_attr="test_value">test</family>'),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = FamilyTag(text, attributes)
        assert repr(tag) == expected

    @pytest.mark.repeat(3)
    def test_get_replacement_value(self, set_random_seed):
        """Test the get_replacement_value method."""
        possible_replacements = {x["value"].lower() for x in FamilyTag.replacement_values}
        random_name = FamilyTag.get_replacement_value(None)

        assert any(name.lower() in random_name.lower() for name in possible_replacements)

    @pytest.mark.parametrize(("orginal_values"), [{"Bloggs", " bloggs "}])
    @pytest.mark.repeat(3)
    def test_get_replacement_mapping(self, set_random_seed, orginal_values):
        """Test the get_replacement_mapping method."""
        possible_replacements = {x["value"].lower() for x in FamilyTag.replacement_values}
        orginal_tags = set()
        for initial_value in orginal_values:
            orginal_tags.add(FamilyTag(initial_value))
        mapping = FamilyTag.get_replacement_mapping(None, orginal_tags)

        for orginal, replacement in mapping.items():
            assert type(orginal) is type(replacement)
            assert orginal.attributes == replacement.attributes
            assert replacement.text.strip().lower() in possible_replacements
            assert orginal.text.isupper() == replacement.text.isupper()
            assert orginal.text.islower() == replacement.text.islower()

            assert len(orginal.text) - len(orginal.text.lstrip()) == len(replacement.text) - len(
                replacement.text.lstrip()
            )
            assert len(orginal.text) - len(orginal.text.rstrip()) == len(replacement.text) - len(
                replacement.text.rstrip()
            )


class TestGivenTag:
    """Test the GivenTag class.

    Does not have any unique logic so skips most of the tests.
    """

    def test_name(self):
        """Test the name property."""
        tag = GivenTag()
        assert tag.name == "given"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<given />"),
            ("test", None, "<given>test</given>"),
            ("test", {"test_attr": "test_value"}, '<given test_attr="test_value">test</given>'),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = GivenTag(text, attributes)
        assert repr(tag) == expected

    @pytest.mark.repeat(3)
    def test_get_replacement_value(self, set_random_seed):
        """Test the get_replacement_value method."""
        possible_replacements = {x["value"].lower() for x in GivenTag.replacement_values}
        random_name = GivenTag.get_replacement_value(None)

        assert any(name.lower() in random_name.lower() for name in possible_replacements)


class TestPrefixTag:
    """Test the PrefixTag class.

    Does not have any unique logic so skips most of the tests.
    """

    def test_name(self):
        """Test the name property."""
        tag = PrefixTag()
        assert tag.name == "prefix"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<prefix />"),
            ("test", None, "<prefix>test</prefix>"),
            ("test", {"test_attr": "test_value"}, '<prefix test_attr="test_value">test</prefix>'),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = PrefixTag(text, attributes)
        assert repr(tag) == expected

    @pytest.mark.repeat(3)
    def test_get_replacement_value(self, set_random_seed):
        """Test the get_replacement_value method."""
        possible_replacements = {x["value"].lower() for x in PrefixTag.replacement_values}
        random_name = PrefixTag.get_replacement_value(None)

        assert any(name.lower() in random_name.lower() for name in possible_replacements)


class TestSuffixTag:
    """Test the SuffixTag class.

    Does not have any unique logic so skips most of the tests.
    """

    def test_name(self):
        """Test the name property."""
        tag = SuffixTag()
        assert tag.name == "suffix"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<suffix />"),
            ("test", None, "<suffix>test</suffix>"),
            ("test", {"test_attr": "test_value"}, '<suffix test_attr="test_value">test</suffix>'),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = SuffixTag(text, attributes)
        assert repr(tag) == expected

    @pytest.mark.repeat(3)
    def test_get_replacement_value(self, set_random_seed):
        """Test the get_replacement_value method."""
        possible_replacements = {x["value"].lower() for x in SuffixTag.replacement_values}
        random_name = SuffixTag.get_replacement_value(None)

        assert any(name.lower() in random_name.lower() for name in possible_replacements)


class TestStreetAddressLineTag:
    """Test the StreetAddressLineTag class."""

    def test_name(self):
        """Test the name property."""
        tag = StreetAddressLineTag()
        assert tag.name == "streetAddressLine"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<streetAddressLine />"),
            ("test", None, "<streetAddressLine>test</streetAddressLine>"),
            (
                "test",
                {"test_attr": "test_value"},
                '<streetAddressLine test_attr="test_value">test</streetAddressLine>',
            ),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = StreetAddressLineTag(text, attributes)
        assert repr(tag) == expected

    @pytest.mark.repeat(3)
    def test_get_replacement_value(self, set_random_seed):
        """Test the get_replacement_value method.

        This method makes an entirely random street address. The only thing to really test is
        whether it contains a street name and type from the YAML files.
        """
        possible_street_names = {
            street["value"].lower() for street in StreetAddressLineTag._street_names
        }
        possible_street_types = {
            street_type["value"].lower() for street_type in StreetAddressLineTag._street_types
        }

        random_address = StreetAddressLineTag.get_replacement_value(None)

        assert any(
            street_name.lower() in random_address.lower() for street_name in possible_street_names
        )
        assert any(
            street_type.lower() in random_address.lower() for street_type in possible_street_types
        )


class TestCityTag:
    """Test the CityTag class.

    Does not have any unique logic so skips most of the tests.
    """

    def test_name(self):
        """Test the name property."""
        tag = CityTag()
        assert tag.name == "city"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<city />"),
            ("test", None, "<city>test</city>"),
            (
                "test",
                {"test_attr": "test_value"},
                '<city test_attr="test_value">test</city>',
            ),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = CityTag(text, attributes)
        assert repr(tag) == expected

    @pytest.mark.repeat(3)
    def test_get_replacement_value(self, set_random_seed):
        """Test the get_replacement_value method."""
        possible_replacements = {x["value"].lower() for x in CityTag.replacement_values}
        random_name = CityTag.get_replacement_value(None)

        assert any(name.lower() in random_name.lower() for name in possible_replacements)


class TestCountyTag:
    """Test the CountyTag class.

    Does not have any unique logic so skips most of the tests.
    """

    def test_name(self):
        """Test the name property."""
        tag = CountyTag()
        assert tag.name == "county"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<county />"),
            ("test", None, "<county>test</county>"),
            (
                "test",
                {"test_attr": "test_value"},
                '<county test_attr="test_value">test</county>',
            ),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = CountyTag(text, attributes)
        assert repr(tag) == expected

    @pytest.mark.repeat(3)
    def test_get_replacement_value(self, set_random_seed):
        """Test the get_replacement_value method."""
        possible_replacements = {x["value"].lower() for x in CountyTag.replacement_values}
        random_name = CountyTag.get_replacement_value(None)

        assert any(name.lower() in random_name.lower() for name in possible_replacements)


class TestStateTag:
    """Test the StateTag class.

    Does not have any unique logic so skips most of the tests.
    """

    def test_name(self):
        """Test the name property."""
        tag = StateTag()
        assert tag.name == "state"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<state />"),
            ("test", None, "<state>test</state>"),
            (
                "test",
                {"test_attr": "test_value"},
                '<state test_attr="test_value">test</state>',
            ),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = StateTag(text, attributes)
        assert repr(tag) == expected

    @pytest.mark.repeat(3)
    def test_get_replacement_value(self, set_random_seed):
        """Test the get_replacement_value method."""
        possible_replacements = {x["value"].lower() for x in StateTag.replacement_values}
        random_name = StateTag.get_replacement_value(None)

        assert any(name.lower() in random_name.lower() for name in possible_replacements)


class TestCountryTag:
    """Test the CountryTag class.

    Does not have any unique logic so skips most of the tests.
    """

    def test_name(self):
        """Test the name property."""
        tag = CountryTag()
        assert tag.name == "country"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<country />"),
            ("test", None, "<country>test</country>"),
            (
                "test",
                {"test_attr": "test_value"},
                '<country test_attr="test_value">test</country>',
            ),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = CountryTag(text, attributes)
        assert repr(tag) == expected

    @pytest.mark.repeat(3)
    def test_get_replacement_value(self, set_random_seed):
        """Test the get_replacement_value method."""
        possible_replacements = {x["value"].lower() for x in CountryTag.replacement_values}
        random_name = CountryTag.get_replacement_value(None)

        assert any(name.lower() in random_name.lower() for name in possible_replacements)


class TestPostalCodeTag:
    """Test the PostalCodeTag class."""

    def test_name(self):
        """Test the name property."""
        tag = PostalCodeTag()
        assert tag.name == "postalCode"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<postalCode />"),
            ("test", None, "<postalCode>test</postalCode>"),
            (
                "test",
                {"test_attr": "test_value"},
                '<postalCode test_attr="test_value">test</postalCode>',
            ),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = PostalCodeTag(text, attributes)
        assert repr(tag) == expected

    @pytest.mark.repeat(3)
    def test_get_replacement_value(self, set_random_seed):
        """Test the get_replacement_value method.

        The current implentation randomly makes a 5 or 9 digit zip code. The only things to test are
        the replacement value is either 5 digits or 5 digits followed by a hyphen and 4 digits.
        """
        random_zip = PostalCodeTag.get_replacement_value(None)

        if len(random_zip) == 5:
            assert random_zip.isdigit()
        elif len(random_zip) == 10:
            assert random_zip[0:5].isdigit()
            assert random_zip[5] == "-"
            assert random_zip[6:10].isdigit()
        else:
            pytest.fail("Invalid zip code length")


class TestTelecomTag:
    """Test the TelecomTag class."""

    def test_name(self):
        """Test the name property."""
        tag = TelecomTag()
        assert tag.name == "telecom"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<telecom />"),
            ("test", None, "<telecom>test</telecom>"),
            (
                "test",
                {"test_attr": "test_value"},
                '<telecom test_attr="test_value">test</telecom>',
            ),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = TelecomTag(text, attributes)
        assert repr(tag) == expected

class TestNameTag:
    """Test the NameTag class."""

    def test_name(self):
        """Test the name property."""
        tag = NameTag()
        assert tag.name == "name"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<name />"),
            ("test", None, "<name>test</name>"),
            (
                "test",
                {"test_attr": "test_value"},
                '<name test_attr="test_value">test</name>',
            ),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = NameTag(text, attributes)
        assert repr(tag) == expected


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


class TestLowTag:
    """Test the LowTag class."""

    def test_name(self):
        """Test the name property."""
        tag = LowTag()
        assert tag.name == "low"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<low />"),
            ("test", None, "<low>test</low>"),
            (
                "test",
                {"test_attr": "test_value"},
                '<low test_attr="test_value">test</low>',
            ),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = LowTag(text, attributes)
        assert repr(tag) == expected


class TestHighTag:
    """Test the HighTag class."""

    def test_name(self):
        """Test the name property."""
        tag = HighTag()
        assert tag.name == "high"

    @pytest.mark.parametrize(
        ("text", "attributes", "expected"),
        [
            (None, None, "<high />"),
            ("test", None, "<high>test</high>"),
            (
                "test",
                {"test_attr": "test_value"},
                '<high test_attr="test_value">test</high>',
            ),
        ],
    )
    def test_repr(self, text, attributes, expected):
        """Test the __repr__ method."""
        tag = HighTag(text, attributes)
        assert repr(tag) == expected
