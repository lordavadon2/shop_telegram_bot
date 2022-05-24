from telebot.types import KeyboardButton, ReplyKeyboardMarkup

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
        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):
        """
        Создает и возвращает разметку кнопок в основном меню
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        item_btn_1 = self.set_btn('CHOOSE_GOODS')
        item_btn_2 = self.set_btn('INFO')
        item_btn_3 = self.set_btn('SETTINGS')
        self.markup.row(item_btn_1)
        self.markup.row(item_btn_2, item_btn_3)
        return self.markup

    def info_menu(self):
        """
        Создает разметку кнопок в меню 'О магазине'
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        item_btn1 = self.set_btn('<<')
        self.markup.row(item_btn1)
        return self.markup

    def settings_menu(self):
        """
        Создает разметку кнопок в меню 'Настройки'
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        item_btn1 = self.set_btn('<<')
        self.markup.row(item_btn1)
        return self.markup
