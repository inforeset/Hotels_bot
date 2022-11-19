from telebot import BaseMiddleware


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool):
        super().__init__()
        self.session_pool = session_pool
        self.update_types = ['message', 'edited_message', 'callback_query']

    def pre_process(self, message, data):
        session = self.session_pool()
        data["session"] = session

    def post_process(self, message, data, exception=None):
        session = data.get("session")
        if session:
            session.close()
