from abc import ABC, abstractmethod


class JsonParserContract(ABC):
    @abstractmethod
    def from_string(self, string: str) -> object:
        pass

    @abstractmethod
    def to_string(self, json: object) -> str:
        pass

