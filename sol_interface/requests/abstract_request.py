import abc


class Request(abc.ABC):
    @abc.abstractmethod
    def request(self, *args) -> dict:
        pass