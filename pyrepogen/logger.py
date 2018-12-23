'''
Created on 20.12.2018

@author: Haz
'''

import logging


TIP_LVL_NUM = 21
WIZARD_LVL_NUM = 22
CHECKPOINT_LVL_NUM = 23



def get_logger(name):
    logging.addLevelName(TIP_LVL_NUM, "TIP")
    logging.Logger.tip = tip
    logging.addLevelName(WIZARD_LVL_NUM, "WIZARD")
    logging.Logger.wizard = wizard
    logging.addLevelName(CHECKPOINT_LVL_NUM, "CHECKPOINT")
    logging.Logger.checkpoint = checkpoint
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s: [%(levelname)s]: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger


def tip(self, message, *args, **kws):
    if self.isEnabledFor(TIP_LVL_NUM):
        self._log(TIP_LVL_NUM, message, args, **kws) 
        
        
def wizard(self, message, *args, **kws):
    if self.isEnabledFor(WIZARD_LVL_NUM):
        self._log(WIZARD_LVL_NUM, message, args, **kws) 
        
        
def checkpoint(self, message, *args, **kws):
    if self.isEnabledFor(CHECKPOINT_LVL_NUM):
        self._log(CHECKPOINT_LVL_NUM, message, args, **kws) 