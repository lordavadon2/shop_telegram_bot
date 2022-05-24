import abc
from markup.markup import Keyboards
from db.dbalchemy import DBManager


class Handler(metaclass=abc.ABCMeta):
    def __init__(self, bot):
        self.bot = bot
        self.keyboard = Keyboards()
        self.db = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass
