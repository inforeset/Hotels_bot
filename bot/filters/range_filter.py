from telebot import AdvancedCustomFilter, types


class MessageInRangeFilter(AdvancedCustomFilter):

    key = 'in_range'

    def check(self, message, text: int):
        if isinstance(message, types.CallbackQuery):
            mes = message.message.text
        else:
            mes = message.text
        if mes.isdigit():
            return int(mes) in range(1, text + 1)
        return False
