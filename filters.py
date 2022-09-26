from telebot import AdvancedCustomFilter, types


class IsPrivateChatFilter(AdvancedCustomFilter):
    """
    Check whether chat_id corresponds to given chat_type.
    .. code-block:: python3
        :caption: Example on using this filter:
        @bot.message_handler(is_private=True)
        # your function
    """

    key = 'is_private'

    def check(self, message, text):
        """
        :meta private:
        """
        if isinstance(message, types.CallbackQuery):
            return message.message.chat.type == 'private'
        return message.chat.type == 'private'
