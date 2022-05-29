import logging

_format = logging.Formatter('%(asctime)-30s %(levelname)-10s %(filename)-10s %(message)s')

LOGGER = logging.getLogger('client')
LOGGER.setLevel(logging.DEBUG)

LOG_FILE = logging.FileHandler('log/client.log', encoding='utf-8')
LOG_FILE.setFormatter(_format)
LOG_FILE.setLevel(logging.DEBUG)

LOGGER.addHandler(LOG_FILE)
