import argparse
import socket
import sys
import time
import log.client_log_config
import logging

from common.settings import *
from common.utils import *

LOG = logging.getLogger('client')


def answer_handler(message: dict) -> str:
    """Server response parsing.

    Args:
        message: Dict with service information server answer.

    Returns: String with status code.
    """

    if message[RESPONSE] == 200:
        LOG.info('Successful answer from server')
        return '200 | OK'
    LOG.warning('Server connection issues')
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
            STATUS: status
        }
    }

    LOG.debug('Presence message is formed')

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
        LOG.critical(f'Wrong server port number - {port}')
        sys.exit(1)
    except socket.error:
        LOG.critical(f'Wrong server IP - {addr}')
        sys.exit(1)

    # Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((addr, port))

    # Transport
    msg = create_presence()
    msg_sender(client_socket, msg)

    response = answer_handler(msg_reader(client_socket))

    LOG.debug(response)


if __name__ == '__main__':
    LOG.info('Client started')
    main()
