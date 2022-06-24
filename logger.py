import logging


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logger.level)
    formatter = logging.Formatter("%(levelname)s %(asctime)s [%(name)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
