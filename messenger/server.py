import argparse
import logging
import select
import socket
import sys
import time

import log.server_log_config
from common.settings import *
from common.utils import *
from decos import log

LOG = logging.getLogger('server')


@log
def client_message_handler(message: dict, all_messages: list, client) -> None:
    """Check message from client and return correct answer.

    Args:
        message: Message from client.
        all_messages: List of all messages to receive.
        client: Current client socket.
    """
    if ACTION in message and TIME in message and ACCOUNT_NAME in message:
        if message[ACTION] == PRESENCE:
            LOG.debug(f'Valid message presence received from client - {message[ACCOUNT_NAME]}')
            send_msg(client, {RESPONSE: 200})
        elif message[ACTION] == MESSAGE:
            all_messages.append({'username': message[ACCOUNT_NAME], 'msg_text': message[MSG_TEXT]})
        else:
            LOG.warning('Incorrect message received from client')
            send_msg(client, {RESPONSE: 400, ERROR: 'Bad request'})


def arg_parser_srv():
    """Function for parsing start app arguments.

    Returns: IP address and port.
    """
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

    return addr, port


def main():
    # Argument parser
    addr, port = arg_parser_srv()

    # Socket
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_socket.bind((addr, port))
    srv_socket.settimeout(0.5)
    LOG.info(f'Server started on {addr}:{port}.')

    all_clients = []
    all_messages = []

    # Listening
    srv_socket.listen(MAX_CONNECTIONS)
    print(f'Server started on {addr}:{port}...')

    while True:
        try:
            client, client_addr = srv_socket.accept()
        except OSError:
            pass
        else:
            all_clients.append(client)
            LOG.info(f'Client {client.getpeername()} connected.')

        read_clients = []
        send_clients = []

        if all_clients:
            read_clients, send_clients, _ = select.select(all_clients, all_clients, [])

        if read_clients:
            for client in read_clients:
                try:
                    client_message_handler(read_msg(client), all_messages, client)
                except:
                    LOG.info(f'Client {client.getpeername()} disconnected')
                    all_clients.remove(client)

        if send_clients and all_messages:
            for msg in all_messages:
                msg_to_send = {
                    ACTION: MESSAGE,
                    SENDER: msg['username'],
                    TIME: time.time(),
                    MSG_TEXT: msg['msg_text']
                    }
                all_messages.remove(msg)
                for client in send_clients:
                    try:
                        send_msg(client, msg_to_send)
                    except:
                        all_clients.remove(client)
                        LOG.info(f'Client {client.getpeername()} disconnected')


if __name__ == '__main__':
    main()
