"""ValueSetRegistry."""

import csv
from pathlib import Path
from typing import ClassVar


class ValueSetRegistry:
    """Singleton to manage valuesets."""

    _instance = None
    _valuesets: ClassVar[dict[str, dict[str, dict[str, str]]]] = {}

    def __new__(cls):
        """Create a singleton instance of ValueSetRegistry."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_valueset(self, valueset_name: str) -> dict[str, dict[str, str]]:
        """Load a valueset from a file or API if not already loaded."""
        if valueset_name not in self._valuesets:
            # Load from file, database, or API call
            valueset_path = Path(f"src/CDA/loinc/{valueset_name}.csv")
            if valueset_path.exists():
                with open(valueset_path) as f:
                    reader = csv.reader(f)
                    next(reader, None)
                    data: dict[str, dict[str, str]] = {}
                    for row in reader:
                        data[row[0]] = {
                            "system": "http://loinc.org",
                            "display": row[1],
                        }
                self._valuesets[valueset_name] = data
            else:
                # Could call a terminology service API instead
                raise ValueError(f"Valueset {valueset_name} not found")
        return self._valuesets[valueset_name]

    def get_code(self, valueset_name: str, code: str) -> dict[str, str]:
        """Get a specific code from a valueset."""
        valueset = self.load_valueset(valueset_name)
        if code in valueset:
            return valueset[code]
        else:
            raise ValueError(f"Code {code} not found in valueset {valueset_name}")
