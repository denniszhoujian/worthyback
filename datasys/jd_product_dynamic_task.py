# encoding: utf-8

import sys
import time

from datasys import timeHelper
import jd_list_crawler
import dbhelper


reload(sys)
sys.setdefaultencoding('utf8')

SLEEP_TIME = 1

def __load_white_categories___():
    sql = 'select category_id from jd_category_white_list limit 100'
    retrows = dbhelper.executeSqlRead(sql)
    retlist = []
    for row in retrows:
        retlist.append(row['category_id'])
    return retlist

def __expand_to_sub_categories__(category_id):
    sql = 'select distinct id from jd_category where id like "%s%%"' %category_id
    retrows = dbhelper.executeSqlRead(sql)
    retlist = []
    for row in retrows:
        retlist.append(row['id'])
    return retlist

def __is_unique_in_list__(id,id_list):
    for item in id_list:
        if item.find(id)==0 and len(item)!=len(id):
            return 0
    return 1

def __remove_duplicate_categories__(category_list):
    retlist = []
    for cat in category_list:
        if __is_unique_in_list__(cat,category_list)==1:
            retlist.append(cat)
    return retlist

def __record_category_task_complete(category_id):
    sql = 'insert into jd_item_dynamic_job(category_id,update_time) values("%s","%s")' %(category_id, timeHelper.getNowLong())
    affected_rows = dbhelper.executeSqlWrite1(sql)
    return affected_rows

def __is_category_already_crawled__(category_id):
    sql = 'select * from jd_item_dynamic_job where category_id="%s" and update_time>="%s 0:00:00"' %(category_id,
                                                                                                     timeHelper.getNow())
    retrows = dbhelper.executeSqlRead(sql)
    if len(retrows)==0:
        return 0
    return 1

def __get_category_list_already_crawled__():
    sql = 'select category_id from jd_item_dynamic_job where update_time>="%s 0:00:00"' %(timeHelper.getNow())
    retrows = dbhelper.executeSqlRead(sql)
    catlist = []
    for row in retrows:
        catlist.append(row['category_id'])
    return catlist

def __remove_completed_tasks__(task_list):
    done_list = __get_category_list_already_crawled__()
    return list(set(task_list)-set(done_list))


def doTaskOnce():
    cat_list = __load_white_categories___()
    sub_cat_list = []
    for cat_id in cat_list:
        sub_cat_list = sub_cat_list + __expand_to_sub_categories__(cat_id)
    task_list = __remove_duplicate_categories__(sub_cat_list)
    total_tasks = len(task_list)
    # print task_list
    print '%s - Total categories expanded = %s' %(timeHelper.getNowLong(),total_tasks)
    task_list2 = __remove_completed_tasks__(task_list)
    print '%s - Total categories to crawl = %s' %(timeHelper.getNowLong(),len(task_list2))

    is_success = 1

    for cat_id in task_list2:
        # if __is_category_already_crawled__(cat_id) > 0:
        #     print 'already crawled, now skip: cat_id: %s' %cat_id
        #     continue
        ret = jd_list_crawler.crawl_category(cat_id)
        time.sleep(SLEEP_TIME)
        print ret
        if ret['status'] == 0:
            __record_category_task_complete(cat_id)
            print 'recorded task complete: %s' %cat_id
        else:
            print '%s - error!' %(timeHelper.getNowLong())
            is_success = 0
    return is_success


def doTask():

    while True:
        t1 = time.time()
        doTaskOnce()
        t2 = time.time()
        remaining = timeHelper.getTimeLeftTillTomorrow()
        print '='*80
        print '%s - Finished crawling, using time: %s seconds' %(timeHelper.getNowLong(),t2-t1)
        print 'Now sleeping for %s seconds till tomorrow' %(remaining)
        print '='*80
        time.sleep(remaining)


if __name__ == "__main__":
    doTask()