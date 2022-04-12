import sys

import logging.config

LOGGING_DICT = {
    'version': 1,
    'disable_existing_version': False,
    'formatters': {
        'base': {
            'format': '%(asctime)s - [%(levelname)s] - <%(filename)s>.<%(funcName)s>(%(lineno)d) - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'level': logging.DEBUG,
            'formatter': 'base'
        }
    },
    'loggers': {
        'syslog_logger': {
            'handlers': ['console'],
            'level': logging.INFO,
        }
    }
}

logging.config.dictConfig(LOGGING_DICT)
log = logging.getLogger('syslog_logger')
log.setLevel('DEBUG')
