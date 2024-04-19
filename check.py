# -*- coding: utf-8 -*-
import os
from log import logger


def check_root():
    if os.popen("whoami").read() != 'root\n':
        logger.warning(f'')
