from loguru import logger
import os

if not os.environ.get('SPOCK_DEBUG'):
    logger.disable('spocktest')