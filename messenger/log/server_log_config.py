import logging
import logging.handlers
import sys

filename = sys.argv[0].split('/')[-1]

_format = logging.Formatter(f'%(asctime)-30s %(levelname)-10s {filename} %(message)s')

LOGGER = logging.getLogger('server')
LOGGER.setLevel(logging.DEBUG)

LOG_FILE = logging.handlers.TimedRotatingFileHandler('log/server.log', encoding='utf-8', when='midnight')
LOG_FILE.setFormatter(_format)
LOG_FILE.setLevel(logging.DEBUG)

LOGGER.addHandler(LOG_FILE)
