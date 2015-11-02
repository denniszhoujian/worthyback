# encoding: utf-8
import memcache
import sys
import urllib2
import data_config

reload(sys)
sys.setdefaultencoding('utf8')

MEMCACHE_URL_LIST = data_config.MEMCACHE_ADDR_LIST
# memcached -m 64 -p 11211 -u memcache -l 127.0.0.1 -d

global __mc__
__mc__ = memcache.Client(MEMCACHE_URL_LIST,debug=0)

class memcachedStatic():

    def __init__(self):
        pass

    @staticmethod
    def getMemCache():
        return __mc__

    @staticmethod
    def getKey(keyname):
        tt = keyname
        try:
            tt = urllib2.quote(keyname.encode('utf-8'))
        except:
            pass
        return tt


if __name__ == '__main__':

    mc = memcachedStatic.getMemCache()
    mc.set('okok',2)
    print mc.get('okok')

    tt = '中文text'
    print urllib2.quote(tt)