from settings.message import MESSAGES
from settings import config
from handlers.handler import Handler


class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_button_category(self, message):
        """
        Обработка нажатия на кнопку 'Выбрать товар'
        """
        self.bot.send_message(message.chat.id, "Каталог категорий товара",
                              reply_markup=self.keyboard.remove_menu())
        self.bot.send_message(message.chat.id, "Сделайте свой выбор",
                              reply_markup=self.keyboard.category_menu())

    def pressed_button_product(self, message, product):
        """
        Обработка нажатия на кнопку 'Выбрать товар'
        """
        self.bot.send_message(message.chat.id, 'Категория ' +
                              config.KEYBOARD[product],
                              reply_markup=
                              self.keyboard.set_select_category(
                                  config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ок",
                              reply_markup=self.keyboard.category_menu())

    def pressed_button_info(self, message):
        """
        Обрабатывает нажатия на кнопку 'О магазине'.
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode="HTML",
                              reply_markup=self.keyboard.info_menu())

    def pressed_button_settings(self, message):
        """
        Обрабатывает нажатия на кнопку 'Настройки'.
        """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keyboard.settings_menu())

    def pressed_button_back(self, message):
        """
        Обрабатывает нажатия на кнопку 'Назад'.
        """
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keyboard.start_menu())

    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие текстовые сообщения от нажатия кнопок.
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_button_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_button_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_button_back(message)

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_button_category(message)

            # ----------------------------------------------#

            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_button_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_button_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_button_product(message, 'ICE_CREAM')
