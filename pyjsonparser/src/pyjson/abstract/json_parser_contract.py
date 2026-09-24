"""Abstract contract definition for JSON parsing and serialization."""

from abc import ABC, abstractmethod


class JsonParserContract(ABC):
    """Abstract base contract for high-level JSON parsers.

    Defines the public interface required for converting between JSON formatted
    strings and native Python data structures.
    """

    @abstractmethod
    def from_string(self, string: str) -> object:
        """Parses a JSON string into a Python data structure.

        Args:
            string: A valid JSON formatted string.

        Returns:
            The parsed Python representation (e.g. dict, list, primitive).

        Raises:
            Exception: If the string is malformed or cannot be parsed.
        """
        pass

    @abstractmethod
    def to_string(self, json: object) -> str:
        """Serializes a Python object into a JSON formatted string.

        Args:
            json: The Python object (dict, list, str, int, float, bool, None)
                to convert into JSON.

        Returns:
            A valid JSON string representation of the object.
        """
        pass
