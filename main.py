from telebot import TeleBot

from settings import config
from handlers.handler_main import HandlerMain


class ShopBot:
    """
    Основной класс телеграмм бота (сервер), в основе которого
    используется библиотека pyTelegramBotAPI
    """
    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self):
        """
        Инициализация бота
        """
        self.token = config.TOKEN
        self.bot = TeleBot(self.token)
        self.handler = HandlerMain(self.bot)

    def start(self):
        """
        Метод предназначен для старта обработчика событий
        """
        self.handler.handle()

    def run_bot(self):
        """
        Метод запускает основные события сервера
        """
        self.start()
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    bot = ShopBot()
    bot.run_bot()
