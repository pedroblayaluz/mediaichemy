import logging


class LoggerSetup:
    LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    @classmethod
    def setup(cls, level='debug'):
        log_level = cls.LEVELS.get(level.lower(), logging.DEBUG)

        logging.root.handlers = []

        debug_handler = logging.StreamHandler()
        debug_handler.setFormatter(logging.Formatter('%(asctime)s | DEBUG | %(name)s:%(lineno)d:%(message)s'))
        debug_handler.addFilter(lambda r: r.levelno == logging.DEBUG)

        info_handler = logging.StreamHandler()
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))

        logging.root.setLevel(log_level)
        logging.root.addHandler(debug_handler)
        logging.root.addHandler(info_handler)


logger_setup = LoggerSetup.setup
