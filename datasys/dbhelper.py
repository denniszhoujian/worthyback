# encoding: utf-8

import MySQLdb
import datetime
import time
import data_config
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

def getConnection():
    datadict = data_config.DATA_SYS_CONFIG
    conn = MySQLdb.connect(host=datadict['host'], user=datadict['user'], passwd=datadict['passwd'], db=datadict['db'], port=datadict['port'], charset='utf8')
    return conn

def executeSqlWrite1(sql, is_dirty=False):
    conn = getConnection()
    try:
        cursor1 = conn.cursor(MySQLdb.cursors.DictCursor)
        #sql = MySQLdb.escape_string(sql)
        if is_dirty:
            cursor1.execute('set @@session.tx_isolation="read-uncommitted"')
        retrows = cursor1.execute(sql)
        conn.commit()
        affected_rows = cursor1.rowcount
    except Exception as e:
        conn.rollback()
        print e
    finally:
        conn.close()
    return affected_rows

def executeSqlWrite(sql, vlist, is_dirty=False):
    conn = getConnection()
    affected_rows = 0
    try:
        cursor1 = conn.cursor(MySQLdb.cursors.DictCursor)
        if is_dirty:
            cursor1.execute('set @@session.tx_isolation="read-committed"')
        cursor1.execute(sql, vlist)
        conn.commit()
        affected_rows = cursor1.rowcount
    except Exception as e:
        conn.rollback()
        print e
    finally:
        conn.close()
    return affected_rows

def executeSqlWriteMany(sql, vlist, is_dirty=False):
    conn = getConnection()
    affected_rows = 0
    try:
        cursor1 = conn.cursor()
        if is_dirty:
            cursor1.execute('set @@session.tx_isolation="read-committed"')
        cursor1.executemany(sql, vlist)
        conn.commit()
        affected_rows = cursor1.rowcount
    except Exception as e:
        conn.rollback()
        print e
    finally:
        conn.close()
    return affected_rows

def executeSqlRead(sql, is_dirty=False):
    conn = getConnection()
    retrows = {}
    try:
        cursor1 = conn.cursor(MySQLdb.cursors.DictCursor)
        if is_dirty:
            cursor1.execute('set @@session.tx_isolation="read-uncommitted"')
        cursor1.execute(sql)
        retrows = cursor1.fetchall()
    finally:
        conn.close()
    return retrows

def executeSqlRead2(sql, is_dirty=False):
    conn = getConnection()
    retrows = {}
    try:
        cursor1 = conn.cursor()
        if is_dirty:
            cursor1.execute('set @@session.tx_isolation="read-uncommitted"')
        cursor1.execute(sql)
        retrows = cursor1.fetchall()
    finally:
        conn.close()
    return retrows

def executeSqlRead3(sql,vlist):
    conn = getConnection()
    retrows = {}
    try:
        cursor1 = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor1.execute(sql,vlist)
        retrows = cursor1.fetchall()
    finally:
        conn.close()
    return retrows


def CreateTableAsDict(TableName,dic):
    try:
        conn=getConnection()
        cur=conn.cursor()
        COLstr=''   #列的字段
        ROWstr=''  #行字段

        # ColumnStyle=' VARCHAR(20)'
        ColumnStyle=' INT(11)'
        for key in dic.keys():
            COLstr=COLstr+' '+key+ColumnStyle+','
            ROWstr=(ROWstr+'"%s"'+',')%(dic[key])

        #判断表是否存在，存在执行try，不存在执行except新建表，再insert
        try:
            cur.execute("CREATE TABLE %s (%s)"%(TableName,COLstr[:-1]))
            cur.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))
        except Exception as e:
            print e
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def InsertDataFromDict(TableName,dic):
    try:
        conn=getConnection()
        cur=conn.cursor()
        COLstr=''   #列的字段
        ROWstr=''  #行字段

        # ColumnStyle=' VARCHAR(20)'
        ColumnStyle=' INT(11)'
        for key in dic:
            COLstr=COLstr+' '+key+ColumnStyle+','
            ROWstr=(ROWstr+'"%s"'+',')%(dic[key])

        #判断表是否存在，存在执行try，不存在执行except新建表，再insert
        affected_rows = 0
        try:
            affected_rows = cur.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))

        except MySQLdb.Error,e:
            print e
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])