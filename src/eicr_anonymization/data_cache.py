"""Data Cache Module."""

from collections.abc import Iterator

from eicr_anonymization.tags.Tag import Tag


class NormalizedTagGroup:
    """A group of tags with the same normalized text and attributes."""

    def __init__(self, tag: Tag):
        """Initialize a tag group with the first tag.

        Args:
            tag: The initial tag to create the group with

        """
        self._group: set[Tag] = {tag}
        self._type = tag.__class__
        self._normalized_tag = self.type(text=tag.normalized_text, attributes=tag.attributes)

    def __len__(self):
        """Get the number of tags in the group.

        Returns:
            Number of tags in the group

        """
        return len(self._group)

    def __iter__(self) -> Iterator[Tag]:
        """Provide an iterator over the tags in the group.

        Returns:
            Iterator of tags

        """
        return iter(self._group)

    @property
    def type(self) -> Tag:
        """Get the class type of the tags in the group.

        Returns:
            Tag class type

        """
        return self._type

    def add(self, tag: Tag) -> None:
        """Add a tag to the group.

        Args:
            tag: Tag to add to the group

        Raises:
            TypeError: If the tag type does not match the group Tag type

        """
        if isinstance(tag, self.type):
            self._group.add(tag)
        else:
            raise TypeError(f"Tag type {tag.__class__} does not match group type {self.type}.")

    def get_replacement_mapping(self) -> dict[Tag, Tag]:
        """Generate mapping from the orginal tag to the replacement tag.

        Returns:
            Mapping from the orginal tag to the replacement tag.

        """
        return self._type.get_replacement_mapping(self._normalized_tag, self._group)


class NormalizedTagGroups:
    """The main data structure for storing tag instances."""

    def __init__(self):
        """Initialize the data structure."""
        self._groups: dict[int, set[Tag]] = {}

    def __len__(self) -> int:
        """Get the total number of tag groups, i.e., the number of unique normalized tags.

        Returns:
            Number of tag groups, i.e., the number of unique normalized tags

        """
        return len(self._groups)

    def add(self, tag: Tag):
        """Add a tag to the cache."""
        tag_hash = tag.normalized_hash
        if tag_hash not in self._groups:
            self._groups[tag_hash] = NormalizedTagGroup(tag)
        self._groups[tag_hash].add(tag)

    def __iter__(self):
        """Iterate over the cache."""
        yield from self._groups.values()
