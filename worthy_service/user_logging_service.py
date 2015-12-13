# encoding: utf-8

from datasys import dbhelper,timeHelper
import threading

def do_log_user_event(device_id, query, catalog_id):

    catalog_name = ""

    if query is not None and len(query) > 0:
        catalog_id = ""
    else:
        query = ""
        catalog_id = "%s" %catalog_id
        if catalog_id == "_ALL_":
            catalog_name = '全部折扣'
        elif catalog_id == "_EXPENSIVE_":
            catalog_name = '超值折扣'
        else:
            sql2 = 'select * from jd_catalog where catalog_id=%s' %catalog_id
            retrows = dbhelper.executeSqlRead(sql2)
            if len(retrows) > 0:
                catalog_name = retrows[0]['catalog_name']
            else:
                catalog_name = 'Unknown'

    sql_user_event = 'insert into user_events values("%s","%s","%s","%s","%s")' %(device_id,query,catalog_id,catalog_name, timeHelper.getNowLong())
    afr = dbhelper.executeSqlWrite1(sql_user_event)
    print afr
    return afr


def log_user_event_with_thread(device_id, query, catalog_id):
    t1 = threading.Thread(target=do_log_user_event, args=(device_id,query,catalog_id))
    t1.setDaemon(True)
    t1.start()

if __name__ == '__main__':
    log_user_event_with_thread('abc','',26000)
    # do_log_user_event('abc',None,27000)
    # do_log_user_event('abc','电脑',27000)
    import time
    time.sleep(10)




