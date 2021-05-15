from loguru import logger
import os
import sys

logger.remove(0)
logger.add(sys.stdout, colorize=True, format="{level}: <level>{message}</level>")
