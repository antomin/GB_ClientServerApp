import argparse
import logging
import socket
import sys
import time

import log.client_log_config
from common.settings import *
from common.utils import *
from decos import log
from exceptions import ClientModeError, ServerError

LOG = logging.getLogger('client')


@log
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


@log
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
        ACCOUNT_NAME: username,
        STATUS: status
        }

    LOG.debug('Presence message is formed')

    return data


# @log
def create_msg(client_socket: socket, username: str) -> dict:
    """The function generates a message to be sent or closes the connection at the user's command.

    Args:
        client_socket: Socket object of client,
        username: Client username

    Returns: Generated dictionary to be sent to the server
    """

    user_msg = input('Enter your message: ')
    if user_msg == 'q':
        client_socket.close()
        LOG.info('Client logged out.')
        print('You are logged out.')
        sys.exit(0)

    data = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: username,
        MSG_TEXT: user_msg
    }

    return data


def recv_msg(msg: dict) -> None:
    """Receiving message from server.

    Args:
        msg: Decoded dict message.
    """
    if ACTION in msg and msg[ACTION] == MESSAGE and SENDER in msg and MSG_TEXT in msg:
        print(f'{msg[SENDER]}: {msg[MSG_TEXT]}')
        LOG.debug(f'Message from {msg[SENDER]} received')
    else:
        LOG.error('Incorrect message from server.')


def arg_parser_client():
    """Function for parsing start app arguments.

    Returns:
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-a', dest='addr', required=True)
    parser.add_argument('-p', dest='port', required=False, default=DEFAULT_PORT)
    parser.add_argument('-u', dest='username', required=False, default='Guest')
    parser.add_argument('-m', dest='mode', required=False, default='listen')

    args = parser.parse_args()

    try:
        addr, port, username, mode = args.addr, int(args.port), args.username, args.mode
        socket.inet_aton(addr)
        if mode != 'listen' and mode != 'send':
            raise ClientModeError(mode)
        if port < 1024 or port > 65535:
            raise ValueError
    except ValueError:
        LOG.critical(f'Wrong server port number - {port}')
        sys.exit(1)
    except socket.error:
        LOG.critical(f'Wrong server IP - {addr}')
        sys.exit(1)
    except ClientModeError as error:
        LOG.critical(error.text)
        sys.exit(1)

    return addr, port, username, mode


def main():
    # Argument parser
    addr, port, username, mode = arg_parser_client()

    # Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((addr, port))

    # Transport
    msg = create_presence(username)
    send_msg(client_socket, msg)
    response = answer_handler(read_msg(client_socket))
    LOG.info(f'Connected to server {addr}:{port}. Server response - {response}')
    if response != '200 | OK':
        raise ServerError(response[ERROR])

    while True:
        try:
            if mode == 'send':
                send_msg(client_socket, create_msg(client_socket, username))
            elif mode == 'listen':
                recv_msg(read_msg(client_socket))
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            LOG.error('Server connection lost')
            print('Server connection lost')


if __name__ == '__main__':
    LOG.info('Client started')
    main()
