import logging


def setup_logger(name, log_file):
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s")

    handler = logging.FileHandler("logs/" + log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


routes_parsing_logger = setup_logger("routes_parsing_logger", "routes_parsing.log")
trains_parsing_logger = setup_logger("trains_parsing_logger", "trains_parsing.log")
logger = setup_logger("errors", "errors.log")
