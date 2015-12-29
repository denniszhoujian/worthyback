# encoding: utf-8

import logging
import sys

LOGGING_LEVEL = logging.DEBUG

def configLogging(log_name, log_level=LOGGING_LEVEL):

    filename = '/datadisk//tmp/%s_task.log' %(log_name)

    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=filename,
                        filemode='a')

    logging.info('START logging : %s' %log_name)


if __name__ == '__main__':
    configLogging('test_task')
    logging.info('dennis is doing a task...')

