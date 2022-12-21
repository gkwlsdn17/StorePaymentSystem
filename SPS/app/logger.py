import datetime
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s]:[%(lineno)d] %(message)s')
# streamhandler = logging.StreamHandler()
# streamhandler.setFormatter(formatter)
# logger.addHandler(streamhandler)

timehandler = logging.handlers.TimedRotatingFileHandler(filename='./log/logs.log', when='midnight', interval=1, encoding='utf-8')
timehandler.setFormatter(formatter)
timehandler.suffix = '%Y%m%d'
logger.addHandler(timehandler)

