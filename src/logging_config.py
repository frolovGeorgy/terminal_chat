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
        'syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
            'level': logging.INFO,
            'formatter': 'base'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'level': logging.DEBUG,
            'formatter': 'base'
        }
    },
    'loggers': {
        'syslog_logger': {
            'handlers': ['syslog', 'console'],
            'level': logging.INFO,
        }
    }
}

logging.config.dictConfig(LOGGING_DICT)
log = logging.getLogger('syslog_logger')
log.setLevel('DEBUG')
