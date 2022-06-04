import logging
import sys
import traceback

from log import client_log_config, server_log_config

RUN_FILENAME = sys.argv[0].split('/')[-1]

if RUN_FILENAME == 'client.py':
    LOGGER = logging.getLogger('client')
else:
    LOGGER = logging.getLogger('server')


def log(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        LOGGER.debug(f'Function {func.__name__} was called with parameters {args, kwargs}. '
                     f'From module {func.__module__}. '
                     f'Inside function {traceback.format_stack()[0].strip().split()[-1]}')
        return res

    return wrapper
