from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup

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

    @staticmethod
    def remove_menu():
        """
        Удаляет меню
        """
        return ReplyKeyboardRemove()

    def category_menu(self):
        """
        Создает разметку кнопок
        """
        self.markup = ReplyKeyboardMarkup(True, True, row_width=1)
        self.markup.add(self.set_btn('SEMIPRODUCT'))
        self.markup.add(self.set_btn('GROCERY'))
        self.markup.add(self.set_btn('ICE_CREAM'))
        self.markup.row(self.set_btn('<<'), self.set_btn('ORDER'))
        return self.markup

    @staticmethod
    def set_inline_btn(name):
        """
        Создает инлайн-кнопку по входным параметрам
        """
        return InlineKeyboardButton(str(name),
                                    callback_data=str(name.id))

    def set_select_category(self, category):
        """
        Создает инлайн-кнопки в выбранной
        категории товара
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        for item in self.db.select_all_products_category(category):
            self.markup.add(self.set_inline_btn(item))

        return self.markup
