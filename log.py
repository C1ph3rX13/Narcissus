# -*- coding: utf-8 -*-

import sys

from loguru import logger

# Init logger
logger.remove()
logger.add(
    sys.stdout,
    format='<green>[{time:YYYY-MM-DD HH:mm:ss}]</green> <level>{message}</level>',
)
