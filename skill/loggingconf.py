

logging_config = {
	'disable_existing_loggers': False,
	'version': 1,
	'formatters': {
		'simple': {
			'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
		},
	},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'formatter': 'simple',
			'class': 'logging.StreamHandler',
		}
	},
	'loggers': {
		'DEV': {
			'handlers': ['console'],
			'level': 'DEBUG',
		},
		'PRODUCTION': {
			'handlers': ['console'],
			'level': 'WARNING',
		}
	},
}
