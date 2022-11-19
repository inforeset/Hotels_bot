from telebot import types, SimpleCustomFilter


class IsPrivateChatFilter(SimpleCustomFilter):

    key = 'is_private'

    def check(self, message):
        if isinstance(message, types.CallbackQuery):
            return message.message.chat.type == 'private'
        return message.chat.type == 'private'
