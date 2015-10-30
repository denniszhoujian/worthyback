# encoding: utf-8

import logging
import sys
import timeHelper

# timenow = timeHelper.getNow()
# filename = '/tmp/worth_datasys_%s.log' %timenow

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename=filename,
#                     filemode='w')
#
# logging.info('START!')

# logger = logging.getLogger("worthyLog")
# formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', '%a, %d %b %Y %H:%M:%S',)
# file_handler = logging.FileHandler(filename)
# file_handler.setFormatter(formatter)
# stream_handler = logging.StreamHandler(sys.stdout)
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)
#
# logger.setLevel(logging.DEBUG)
#
# def getLogger():
#     return logger

def configLogging(log_name):
    timenow = timeHelper.getNow()
    filename = '/tmp/%s_worthy_%s.log' %(log_name,timenow)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=filename,
                        filemode='a')

    logging.info('START logging : %s' %log_name)


if __name__ == '__main__':
    configLogging('sure')
    logging.info('dennis')

