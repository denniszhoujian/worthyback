# encoding: utf-8
import service_config
import dbhelper_read

def getQueryHistory(device_id):
    sql = 'select distinct query from user_events where device_id="%s" and query is not NULL and query<>"" order by event_time DESC limit %s' %(device_id,service_config.QUERY_HISTORY_MAX_NUM)
    retrows = dbhelper_read.executeSqlRead(sql,is_dirty=True)
    rlist = []
    for row in retrows:
        rlist.append(row['query'])
    return rlist

def getCatalogHistory(device_id):
    sql = 'select distinct catalog_id, catalog_name from user_events where device_id="%s" and catalog_id is not NULL and catalog_id<>"" order by event_time DESC limit %s' %(device_id,service_config.CATALOG_HISTORY_MAX_NUM)
    # print sql
    retrows = dbhelper_read.executeSqlRead(sql,is_dirty=True)

    rlist = []
    for row in retrows:
        rlist.append([row['catalog_id'],row['catalog_name']])
    return rlist

