from telebot.types import KeyboardButton

from db.dbalchemy import DBManager
from settings import config


class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки интерфейса бота
    """
    def __init__(self):
        self.markup = None
        self.db = DBManager()

    def set_btn(self, name, step=0, quantity=0):
        """
        Создает и возвращает конпку по входным параметрам
        """
        return KeyboardButton(config.KEyBOARD[name])