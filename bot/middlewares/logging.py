import logging

from telebot import BaseMiddleware, types

HANDLED_STR = ['Unhandled', 'Handled']

class LoggingMiddleware(BaseMiddleware):

    def __init__(self, logger=__name__):
        self.update_types = ['message', 'edited_message', 'callback_query']
        self.update_sensitive = True
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        self.logger = logger

        super(LoggingMiddleware, self).__init__()

    def pre_process_message(self, message: types.Message, data: dict):
        self.logger.info(f"Received message [ID:{message.message_id}] in chat [{message.chat.type}:{message.chat.id}]")

    def post_process_message(self, message: types.Message, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"message [ID:{message.message_id}] in chat [{message.chat.type}:{message.chat.id}]")

    def pre_process_edited_message(self, edited_message, data: dict):
        self.logger.info(f"Received edited message [ID:{edited_message.message_id}] "
                         f"in chat [{edited_message.chat.type}:{edited_message.chat.id}]")

    def post_process_edited_message(self, edited_message, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"edited message [ID:{edited_message.message_id}] "
                          f"in chat [{edited_message.chat.type}:{edited_message.chat.id}]")

    def pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        if callback_query.message:
            message = callback_query.message
            text = (f"Received callback query [ID:{callback_query.id}] "
                    f"from user [ID:{callback_query.from_user.id}] "
                    f"for message [ID:{message.message_id}] "
                    f"in chat [{message.chat.type}:{message.chat.id}] "
                    f"with data: {callback_query.data}")

            if message.from_user:
                text = f"{text} originally posted by user [ID:{message.from_user.id}]"

            self.logger.info(text)

        else:
            self.logger.info(f"Received callback query [ID:{callback_query.id}] "
                             f"from user [ID:{callback_query.from_user.id}] "
                             f"for inline message [ID:{callback_query.inline_message_id}] ")

    def post_process_callback_query(self, callback_query, results, data: dict):
        if callback_query.message:
            message = callback_query.message
            text = (f"{HANDLED_STR[bool(len(results))]} "
                    f"callback query [ID:{callback_query.id}] "
                    f"from user [ID:{callback_query.from_user.id}] "
                    f"for message [ID:{message.message_id}] "
                    f"in chat [{message.chat.type}:{message.chat.id}] "
                    f"with data: {callback_query.data}")

            if message.from_user:
                text = f"{text} originally posted by user [ID:{message.from_user.id}]"

            self.logger.info(text)

        else:
            self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                              f"callback query [ID:{callback_query.id}] "
                              f"from user [ID:{callback_query.from_user.id}]"
                              f"from inline message [ID:{callback_query.inline_message_id}]")
