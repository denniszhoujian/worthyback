# encoding: utf-8

import MySQLdb
import datetime
import time
from datasys import data_config
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

def getConnection():
    datadict = data_config.DATA_SYS_CONFIG_READ_ONLY
    conn = MySQLdb.connect(host=datadict['host'], user=datadict['user'], passwd=datadict['passwd'], db=datadict['db'], port=datadict['port'], charset='utf8')
    return conn

def executeSqlRead(sql, is_dirty=False, isolation_type="read-uncommitted"):
    conn = getConnection()
    retrows = {}
    try:
        cursor1 = conn.cursor(MySQLdb.cursors.DictCursor)
        if is_dirty:
            cursor1.execute('set @@session.tx_isolation="%s"' %isolation_type)
        cursor1.execute(sql)
        retrows = cursor1.fetchall()
    finally:
        conn.close()
    return retrows

def executeSqlRead2(sql, is_dirty=False, isolation_type="read-uncommitted"):
    conn = getConnection()
    retrows = {}
    try:
        cursor1 = conn.cursor()
        if is_dirty:
            cursor1.execute('set @@session.tx_isolation="%s"' %isolation_type)
        cursor1.execute(sql)
        retrows = cursor1.fetchall()
    finally:
        conn.close()
    return retrows
