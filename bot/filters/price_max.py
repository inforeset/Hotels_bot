from telebot import types, SimpleCustomFilter, TeleBot


class PriceMaxFilter(SimpleCustomFilter):
    '''
    Filter for max_price
    '''

    def __init__(self, bot: TeleBot):
        self.bot = bot

    key = 'price_max'

    def check(self, message):
        """
        :meta private:
        """
        if isinstance(message, types.CallbackQuery):
            mes = message.message
        else:
            mes = message
        if mes.text.isdigit():
            with self.bot.retrieve_data(user_id=mes.from_user.id, chat_id=mes.chat.id) as data:
                price_min = data['price_min']
            return int(mes.text) > price_min
        return False
