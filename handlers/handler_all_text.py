from settings.message import MESSAGES
from settings import config, utility
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

    def pressed_button_order(self, message):
        """
        Обрабатывает нажатия на кнопку 'Заказ'.
        """
        self.step = 0
        count = self.db.get_all_products_id()
        quantity = self.db.select_order_quantity(count[self.step])

        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователю по заказу
        """
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(
            self.step + 1), parse_mode="HTML")
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].
                              format(self.db.select_single_product_name(
                                  product_id),
                                  self.db.select_single_product_title(
                                      product_id),
                                  self.db.select_single_product_price(
                                      product_id),
                                  self.db.select_order_quantity(
                                      product_id)),
                              parse_mode="HTML",
                              reply_markup=self.keyboard.orders_menu(
                                  self.step, quantity))

    def pressed_button_up(self, message):
        """
        Обработка кнопки увеличения
        количества определенного товара в заказе
        """
        count = self.db.get_all_products_id()
        quantity_order = self.db.select_order_quantity(count[self.step])
        quantity_product = self.db.select_single_product_quantity(
            count[self.step])

        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            self.db.update_order_value(count[self.step],
                                       'quantity', quantity_order)
            self.db.update_product_value(count[self.step],
                                         'quantity', quantity_product)

        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_button_down(self, message):
        """
        Обработка кнопки уменьшения
        количества определенного товара в заказе
        """
        count = self.db.get_all_products_id()
        quantity_order = self.db.select_order_quantity(count[self.step])
        quantity_product = self.db.select_single_product_quantity(
            count[self.step])

        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            self.db.update_order_value(count[self.step],
                                       'quantity', quantity_order)
            self.db.update_product_value(count[self.step],
                                         'quantity', quantity_product)

        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_button_del(self, message):
        """
        Обработка кнопки удаления
        товарной позиции заказа
        """
        count = self.db.get_all_products_id()
        if count.__len__() > 0:
            quantity_order = self.db.select_order_quantity(count[self.step])
            quantity_product = self.db.select_single_product_quantity(
                count[self.step])
            quantity_product += quantity_order
            self.db.delete_order(count[self.step])
            self.db.update_product_value(count[self.step],
                                         'quantity', quantity_product)
            self.step -= 1

        count = self.db.get_all_products_id()
        if count.__len__() > 0:
            quantity_order = self.db.select_order_quantity(count[self.step])
            self.send_message_order(count[self.step], quantity_order, message)

        else:
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keyboard.category_menu())

    def pressed_button_back_step(self, message):
        """
        Обработка кнопки перемещения
        к более ранним товарным позициям заказа
        """
        if self.step > 0:
            self.step -= 1

        count = self.db.get_all_products_id()
        quantity = self.db.select_order_quantity(count[self.step])

        self.send_message_order(count[self.step], quantity, message)

    def pressed_button_next_step(self, message):
        """
        Обработка кнопки перемещения
        к более поздним товарным позициям заказа
        """

        if self.step < self.db.count_rows_order() - 1:
            self.step += 1

        count = self.db.get_all_products_id()
        quantity = self.db.select_order_quantity(count[self.step])

        self.send_message_order(count[self.step], quantity, message)

    def pressed_button_aplly(self, message):
        """
        Обрабатывает нажате на кнопку 'Оформить заказ'.
        """
        self.bot.send_message(message.chat.id,
                              MESSAGES['apply'].format(
                                  utility.get_total_coast(self.db),

                                  utility.get_total_quantity(self.db)),
                              parse_mode="HTML",
                              reply_markup=self.keyboard.category_menu())

        self.db.delete_all_order()

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

            if message.text == config.KEYBOARD['ORDER']:
                if self.db.count_rows_order() > 0:
                    self.pressed_button_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode="HTML",
                                          reply_markup=self.keyboard.
                                          category_menu())

            # ----------------------------------------------#

            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_button_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_button_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_button_product(message, 'ICE_CREAM')

            # ----------------------------------------------#

            if message.text == config.KEYBOARD['UP']:
                self.pressed_button_up(message)

            if message.text == config.KEYBOARD['DOWN']:
                self.pressed_button_down(message)

            if message.text == config.KEYBOARD['X']:
                self.pressed_button_del(message)

            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_button_back_step(message)

            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_button_next_step(message)

            if message.text == config.KEYBOARD['APPLY']:
                self.pressed_button_aplly(message)
            else:
                self.bot.send_message(message.chat.id, message.text)
