import argparse
import socket
import sys

from common.settings import *
from common.utils import *


def client_message_handler(message: dict) -> dict:
    """Check message from client and return correct status code.

    Args:
        message: Message from client.

    Returns: Dict with status code.
    """

    if message[ACTION] == PRESENCE and TIME in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {RESPONSE: 400, ERROR: 'Bad request'}


def main():
    # Argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', dest='addr', required=False, default=DEFAULT_IP)
    parser.add_argument('-p', dest='port', required=False, default=DEFAULT_PORT)

    args = parser.parse_args()

    try:
        addr, port = args.addr, int(args.port)
        socket.inet_aton(addr)
        if port < 1024 or port > 65535:
            raise ValueError
    except ValueError:
        print('Wrong port number.')
        sys.exit(1)
    except socket.error:
        print('Wrong IP')
        sys.exit(1)

    # Socket
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_socket.bind((addr, port))

    # Listening
    srv_socket.listen(MAX_CONNECTIONS)

    while True:
        client_socket, client_addr = srv_socket.accept()
        message = msg_reader(client_socket)
        response = client_message_handler(message)
        msg_sender(client_socket, response)


if __name__ == '__main__':
    main()
