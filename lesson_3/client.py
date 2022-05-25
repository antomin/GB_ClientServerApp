import argparse
import socket
import sys
import time

from common.settings import *
from common.utils import *


def answer_handler(message: dict) -> str:
    """Server response parsing.

    Args:
        message: Dict with service information server answer.

    Returns: String with status code.
    """

    if message[RESPONSE] == 200:
        return '200 | OK'
    return f'{message[RESPONSE]} | {message[ERROR]}'


def create_presence(username: str = 'Guest', status: str = 'Online') -> dict:
    """Creating data for presence message.

    Args:
      username: Username with which the client connects.
      status: User states in network.

    Returns: Dict object conforming to the JIM protocol.

    """
    data = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: username,
            'status': status
        }
    }

    return data


def main():
    # Argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', dest='addr', required=True)
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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((addr, port))

    # Transport
    msg = create_presence()
    msg_sender(client_socket, msg)

    response = answer_handler(msg_reader(client_socket))

    print(response)


if __name__ == '__main__':
    main()
