import abc


class Request(abc.ABC):
    def __init__(self, link):
        self.__link = link

    @abc.abstractmethod
    def request(self, *args):
        pass

    @property
    def link(self):
        return self.__link