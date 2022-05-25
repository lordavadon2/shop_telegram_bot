from handlers.handler import Handler

from settings.message import MESSAGES


class HandlerInlineQuery(Handler):
    """
    Класс обрабатывает входящие текстовые
    сообщения от нажатия на инлайн-кнопоки
    """

    def __init__(self, bot):
        super().__init__(bot)

    def pressed_button_product(self, call, code):
        """
        Обрабатывает нажатие inline-кнопок товара
        """
        self.db.add_orders(quantity=1, product_id=code, user_id=1)

        self.bot.answer_callback_query(
            call.id,
            MESSAGES['product_order'].format(
                self.db.select_single_product_name(code),
                self.db.select_single_product_title(code),
                self.db.select_single_product_price(code),
                self.db.select_single_product_quantity(code)),
            show_alert=True)

    def handle(self):
        # обработчик(декоратор) запросов от нажатия на кнопки товара.
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data
            if code.isdigit():
                code = int(code)

            self.pressed_button_product(call, code)
