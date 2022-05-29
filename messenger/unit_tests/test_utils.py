import json
import unittest

from messenger.common.settings import *
from messenger.common.utils import msg_reader, msg_sender


class TestSocket:
    def __init__(self, test_msg):
        self.test_msg = test_msg
        self.encoded_test_msg = None
        self.receved_message = None

    def send(self, msg_to_send):
        json_test_msg = json.dumps(self.test_msg)
        self.encoded_test_msg = json_test_msg.encode(ENCODING)
        self.receved_message = msg_to_send

    def recv(self, max_len):
        json_test_msg = json.dumps(self.test_msg)
        return json_test_msg.encode(ENCODING)


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.msg_to_send = {
            ACTION: PRESENCE,
            TIME: 1,
            USER: {
                ACCOUNT_NAME: 'Guest',
                STATUS: 'Online'
            }
        }
        self.response_ok = {RESPONSE: 200}
        self.response_bad = {RESPONSE: 400, ERROR: 'Bad request'}

    def test_sending(self):
        socket = TestSocket(self.msg_to_send)
        msg_sender(socket, self.msg_to_send)
        self.assertEqual(socket.encoded_test_msg, socket.receved_message)

    def test_reading_ok(self):
        socket = TestSocket(self.response_ok)
        self.assertEqual(msg_reader(socket), self.response_ok)

    def test_reading_bad(self):
        socket = TestSocket(self.response_bad)
        self.assertEqual(msg_reader(socket), self.response_bad)


if __name__ == '__main__':
    unittest.main()
