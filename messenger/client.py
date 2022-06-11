import argparse
import logging
import socket
import sys
import threading
import time

import log.client_log_config
from common.settings import *
from common.utils import *
from decos import log
from exceptions import ClientModeError, ServerError

LOG = logging.getLogger('client')


@log
def client_exit(client_socket: socket) -> None:
    """Close socket and exit

    Args:
        client_socket: Client socket
    """
    client_socket.close()
    LOG.info('Client logged out.')
    print('You are logged out.')
    sys.exit(0)


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


@log
def send_user_msg(client_socket: socket, username: str) -> dict:
    """The function generates a message to be sent or closes the connection at the user's command.

    Args:
        client_socket: Socket object of client,
        username: Client username

    Returns: Generated dictionary to be sent to the server
    """
    while True:
        print('For exit enter "q".')
        recipient_user = input('To whom: ')
        if recipient_user == 'q':
            client_exit(client_socket)
        user_msg = input(f'Enter message for {recipient_user}: ')
        if user_msg == 'q':
            client_exit(client_socket)

        msg = {
            ACTION: MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: username,
            RECIPIENT: recipient_user,
            MSG_TEXT: user_msg
        }

        send_msg(client_socket, msg)


def recv_msg(client_socket: socket, username: str) -> None:
    """Receiving message from server.

    Args:
        client_socket: Client Socket waiting for a message.
        username: Current username.
    """
    while True:
        msg = read_msg(client_socket)
        if RECIPIENT in msg and msg[RECIPIENT] == username and ACTION in msg and msg[ACTION] == MESSAGE \
                and SENDER in msg and MSG_TEXT in msg:
            print(f'\n{msg[SENDER]}: {msg[MSG_TEXT]}')
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

    args = parser.parse_args()

    try:
        addr, port, username = args.addr, int(args.port), args.username
        socket.inet_aton(addr)
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

    return addr, port, username


def main():
    # Argument parser
    addr, port, username = arg_parser_client()

    # Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((addr, port))

    # Transport
    presence_msg = create_presence(username)
    send_msg(client_socket, presence_msg)
    response = answer_handler(read_msg(client_socket))
    LOG.info(f'Connected to server {addr}:{port}. Server response - {response}')
    if response != '200 | OK':
        raise ServerError(response[ERROR])

    thread_read = threading.Thread(target=recv_msg, args=(client_socket, username))
    thread_read.daemon = True
    thread_read.start()

    thread_send = threading.Thread(target=send_user_msg, args=(client_socket, username,))
    thread_send.daemon = True
    thread_send.start()

    thread_read.join()
    thread_send.join()

    while True:
        if thread_send.is_alive() and thread_read.is_alive():
            continue
        break


if __name__ == '__main__':
    LOG.info('Client started')
    main()
