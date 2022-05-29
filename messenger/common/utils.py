import json
import socket

from common.settings import ENCODING, MAX_PACKAGE_LENGTH


def msg_sender(sock: socket, message: dict) -> None:
    """Encoding and sending message from socket.

    Args:
        sock: Socket sender.
        message: Message to send
    """
    json_msg = json.dumps(message)
    sock.send(json_msg.encode(ENCODING))


def msg_reader(sock: socket) -> dict:
    """Receiving and decoding a message.

    Args:
        sock: Socket receiver.

    Returns: Dict object conforming to the JIM protocol.
    """
    raw_response = sock.recv(MAX_PACKAGE_LENGTH)
    json_response = raw_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    raise ValueError
