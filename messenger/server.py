import argparse
import socket
import sys
import logging
import log.server_log_config
from decos import log

from common.settings import *
from common.utils import *

LOG = logging.getLogger('server')


@log
def client_message_handler(message: dict) -> dict:
    """Check message from client and return correct status code.

    Args:
        message: Message from client.

    Returns: Dict with status code.
    """

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        LOG.debug(f'Valid message received from client - {message[USER][ACCOUNT_NAME]}')
        return {RESPONSE: 200}
    LOG.warning('Incorrect message received from client')
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
        LOG.critical(f'Wrong port number {port}')
        sys.exit(1)
    except socket.error:
        LOG.critical(f'Wrong IP {addr}')
        sys.exit(1)

    # Socket
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_socket.bind((addr, port))
    LOG.info(f'Server started on {addr}:{port} ')

    # Listening
    srv_socket.listen(MAX_CONNECTIONS)

    while True:
        client_socket, client_addr = srv_socket.accept()
        LOG.debug(f'Message received from client {client_addr}')
        message = msg_reader(client_socket)
        response = client_message_handler(message)
        msg_sender(client_socket, response)
        LOG.debug(f'Response sent to client {client_addr}')


if __name__ == '__main__':
    main()
