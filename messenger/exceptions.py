class ClientModeError(Exception):
    def __init__(self, mode):
        self.text = f'Invalid client mode - {mode}. Can only be "listen" or "send".'

    def __str__(self):
        return self.text


class ServerError(Exception):
    def __int__(self, text):
        self.text = text

    def __str__(self):
        return f'Bad server response - {self.text}.'
