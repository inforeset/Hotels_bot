from typing import Dict, Any

from telebot import BaseMiddleware, types


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.update_types = ['message', 'edited_message', 'callback_query']

    def pre_process(self, message: types.Message, data: Dict[str, Any]):
        data["config"] = self.config

    def post_process(self, message, data, exception):
        pass