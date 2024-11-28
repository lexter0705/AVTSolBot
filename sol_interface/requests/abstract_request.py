import abc


class Request(abc.ABC):
    def __init__(self, link):
        self.__link = link

    @abc.abstractmethod
    def request(self, *args) -> dict:
        pass

    @property
    def link(self):
        return self.__link