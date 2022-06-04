import unittest

from common.settings import *
from server import client_message_handler


class TestClientMessageHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.message = {ACTION: PRESENCE,
                        TIME: 1,
                        USER: {
                            ACCOUNT_NAME: 'Guest',
                            STATUS: 'Online'
                        }}
        self.response_ok = {RESPONSE: 200}
        self.response_bad = {RESPONSE: 400, ERROR: 'Bad request'}

    def test_client_message_handler_ok(self):
        self.assertEqual(client_message_handler(self.message), self.response_ok)

    def test_other_action(self):
        self.message[ACTION] = 'Hello World!'
        self.assertEqual(client_message_handler(self.message), self.response_bad)

    def test_without_action(self):
        self.message.pop(ACTION)
        self.assertEqual(client_message_handler(self.message), self.response_bad)

    def test_without_time(self):
        self.message.pop(TIME)
        self.assertEqual(client_message_handler(self.message), self.response_bad)

    def test_with_other_account_name(self):
        self.message[USER][ACCOUNT_NAME] = 'TestUser'
        self.assertEqual(client_message_handler(self.message), self.response_bad)

    def test_without_user(self):
        self.message.pop(USER)
        self.assertEqual(client_message_handler(self.message), self.response_bad)


if __name__ == '__main__':
    unittest.main()
