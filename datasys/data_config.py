# encoding: utf-8

#########
# INDEX
# 0: PRODUCTION
# 1: DEV - HOME
# 2: DEV - OUTSIDE
# 3: PROD - TEMP when database is not moved yet
#########

import logging

ACTIVE_PROFILE_INDEX = 4
LOGGING_LEVEL = logging.DEBUG

_profiles_ = [
    # 0: PRODUCTION
    {
        "database_master": {
            'host': 'www.moshutao.cn',
            'user': 'root',
            'passwd': 'Pj24Clep!',
            'db': 'worthyDB',
            'port': 3317
        },
        "database_slave": {
            'host': 'www.moshutao.cn',
            'user': 'root',
            'passwd': 'Pj24Clep!',
            'db': 'worthyDB',
            'port': 3317
        },
        "memcached": ["www.moshutao.cn:13782"],
        "uwsgi_domain": "www.moshutao.com",
        "sphinx": "www.moshutao.cn",
    },
    # 1: DEV - HOME
    {
        "database_master": {
            'host': '192.168.31.100',
            'user': 'root',
            'passwd': 'Pj24Clep!',
            'db': 'worthyDB',
            'port': 3306
        },
        "database_slave": {
            'host': '192.168.31.100',
            'user': 'root',
            'passwd': 'Pj24Clep!',
            'db': 'worthyDB',
            'port': 3306
        },
        "memcached": ["192.168.31.100:11211"],
        "uwsgi_domain": "www.moshutao.com"
    },
    # 2: DEV - OUTSIDE
    {
        "database_master": {
            'host': 'www.moshutao.cn',
            'user': 'root',
            'passwd': 'Pj24Clep!',
            'db': 'worthyDB',
            'port': 3317
        },
        "database_slave": {
            'host': 'www.moshutao.cn',
            'user': 'root',
            'passwd': 'Pj24Clep!',
            'db': 'worthyDB',
            'port': 3317
        },
        "memcached": ["127.0.0.1:11211"],
        "uwsgi_domain": "www.moshutao.com"
    },
    # 3: PRODUCTION - TEMP
    {
        "database_master": {
            'host': 'www.moshutao.cn',
            'user': 'root',
            'passwd': 'Pj24Clep!',
            'db': 'worthyDB',
            'port': 3306
        },
        "database_slave": {
            'host': 'www.moshutao.com',
            'user': 'root',
            'passwd': 'Pj24Clep!',
            'db': 'worthyDB',
            'port': 3317
        },
        "memcached": ["127.0.0.1:11211"],
        "uwsgi_domain": "www.moshutao.com",
    },
    # 4: DEV - HOME - Macbook air
    {
        "database_master": {
            'host': '192.168.31.132',
            'user': 'root',
            'passwd': 'Pj24Clep!',
            'db': 'worthyDB',
            'port': 3306
        },
        "database_slave": {
            'host': '192.168.31.132',
            'user': 'root',
            'passwd': 'Pj24Clep!',
            'db': 'worthyDB',
            'port': 3306
        },
        "memcached": ["192.168.31.100:11211"],
        "uwsgi_domain": "www.moshutao.com",
        "sphinx": "192.168.31.100",
    },

]

DATA_SYS_CONFIG = _profiles_[ACTIVE_PROFILE_INDEX]['database_master']
DATA_SYS_CONFIG_READ_ONLY = _profiles_[ACTIVE_PROFILE_INDEX]['database_slave']
MEMCACHE_ADDR_LIST = _profiles_[ACTIVE_PROFILE_INDEX]['memcached']
SERVER_DOMAIN = _profiles_[ACTIVE_PROFILE_INDEX]['uwsgi_domain']
SPHINX_HOST = _profiles_[ACTIVE_PROFILE_INDEX]['sphinx']

accountSid = "4ff7a5d35b20a0efabb103a1dea89e7c"
accountToken = "9caeceaf5fe4655a9366f143239b427a"

