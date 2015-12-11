# encoding: utf-8

import commands
from datasys.memcachedHelper import memcachedStatic

CORESEEK_PATH = '/usr/local/coreseek/bin/'
ROTATE_INDEX_SHELL_CMD = 'indexer --all --rotate'

def execute_rotate_index():

    cmd = "%s%s" %(CORESEEK_PATH,ROTATE_INDEX_SHELL_CMD)
    output = commands.getstatusoutput(cmd)
    ret = {
        'status': output[0],
        'msg': output[1],
    }
    return ret

def flush_memcache_content():
    mc = memcachedStatic.getMemCache()
    mc.flush_all()

if __name__ == '__main__':

    print execute_rotate_index()
