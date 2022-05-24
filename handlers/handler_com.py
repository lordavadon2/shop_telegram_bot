from .handler import Handler


class HandlerCommands(Handler):
    """
    Класс обробатывает входящие команды /start и /help и т.п.
    """
    def __init__(self, bot):
        super().__init__(bot)

    def pressed_button_start(self, message):
        """
        Обрабатывает входящую /start комманду
        """
        self.bot.send_message(message.chat.id,
                              f'{message.from_user.first_name},'
                              f' здравствуйте! Жду дальнейших задач.',
                              reply_markup=self.keyboard.start_menu())

    def handle(self):
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            if message.text == '/start':
                self.pressed_button_start(message)
