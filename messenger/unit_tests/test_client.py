import unittest

from client import answer_handler, create_presence
from common.settings import *


class TestAnswerHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.answer_200 = {RESPONSE: 200}
        self.answer_400 = {RESPONSE: 400, ERROR: 'Bad request'}
        self.bad_answer = {ERROR: 'No response'}

    def test_ok_answer(self):
        self.assertEqual(answer_handler(self.answer_200), '200 | OK')

    def test_400_answer(self):
        self.assertEqual(answer_handler(self.answer_400), '400 | Bad request')

    def test_without_response(self):
        self.assertRaises(KeyError, answer_handler, self.bad_answer)


class TestCreatePresence(unittest.TestCase):
    def setUp(self) -> None:
        self.time = 1
        self.username = 'Test User'
        self.status = 'ready to speak'

    def test_create_presence_account_info(self):
        self.assertEqual(create_presence(self.username, self.status)[USER], {
            ACCOUNT_NAME: self.username,
            STATUS: self.status
        })

    def test_create_presence_default(self):
        data = create_presence()
        data[TIME] = self.time
        self.assertEqual(data, {
            ACTION: PRESENCE,
            TIME: self.time,
            USER: {
                ACCOUNT_NAME: 'Guest',
                STATUS: 'Online'
            }
        })


if __name__ == '__main__':
    unittest.main()
