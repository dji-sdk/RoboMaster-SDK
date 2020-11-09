import sys
import time

if sys.version_info < (3, 6, 5):
    sys.exit('RoboMaster Sdk requires Python 3.6.5 or later')

import logging

logger_name = "multi_robot"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.ERROR)
fmt = "%(asctime)-15s %(levelname)s %(filename)s:%(lineno)d %(message)s"
formatter = logging.Formatter(fmt)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)


def enable_logging_to_file():
    logger.setLevel(logging.INFO)
    filename = "RoboMasterSDK_MultiRobot_{0}_log.txt".format(time.strftime("%Y%m%d%H%M%S", time.localtime()))
    fh = logging.FileHandler(filename)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


__all__ = ['multi_robot', 'multi_group', 'multi_module', 'tool']
