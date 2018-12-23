'''
Created on 20.12.2018

@author: Haz
'''

from .logger import get_logger

logger = get_logger(__name__)


def mod1_msg():
    logger.info("Hello from mod1!")