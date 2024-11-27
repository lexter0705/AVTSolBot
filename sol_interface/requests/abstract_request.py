import abc


class Request(abc.ABC):
    def __init__(self, link):
        self.__link = link

    @abc.abstractmethod
    def request(self, *args) -> dict:
        pass

    def get_link(self):
        return self.__link