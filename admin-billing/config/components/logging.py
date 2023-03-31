import logging
from logging import config as logging_config


logger = logging.getLogger('django.db.backends')
log_hook = logging.getLogger('django_hook')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': 'DJANDO_HOOK [%(module)s: %(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'console_verbose': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'django_hook': {
            'level': 'DEBUG',
            'handlers': ['console_verbose'],
        },
    }
}


logging_config.dictConfig(LOGGING)
