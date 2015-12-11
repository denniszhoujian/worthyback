# encoding: utf-8

import commands
from datasys.memcachedHelper import memcachedStatic
from worthy_service import catalog_service,sku_service

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

def re_cache():
    clist = catalog_service.getCatalogs()
    for item in clist:
        catalog_id = item['category_id']
        sku_service.getSkuListByCatalogID(catalog_id,startpos=0)

if __name__ == '__main__':
    print "step 1"
    print execute_rotate_index()
    print "step 2"
    flush_memcache_content()
    print 'step 3'
    re_cache()
    print "step 4"
