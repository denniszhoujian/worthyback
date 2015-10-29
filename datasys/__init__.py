import logging

from datasys import timeHelper


timenow = timeHelper.getNowLong()
filename = '/tmp/worth_datasys_%s.log' %timenow

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=filename,
                    filemode='w')


