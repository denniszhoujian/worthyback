# encoding: utf-8

import sys
import dbhelper
import time
from task_class import DataTask
import jd_list_crawler
import mylog

reload(sys)
sys.setdefaultencoding('utf8')

mylog.configLogging('list_task')

class Jd_List_DataTask(DataTask):

     # VIRTUAL
    def __load_all_tasks__(self):
        cat_list = __load_white_categories___()
        sub_cat_list = []
        for cat_id in cat_list:
            sub_cat_list = sub_cat_list + __expand_to_sub_categories__(cat_id)
        task_list = __remove_duplicate_categories__(sub_cat_list)
        return task_list

    # VIRTUAL
    def __task_order__(self,task_id):
        return jd_list_crawler.crawl_category(task_id)

#
# ==================================================================================
#

def __load_white_categories___():
    sql = 'select category_id from jd_category_white_list limit 100'
    retrows = dbhelper.executeSqlRead(sql)
    retlist = []
    for row in retrows:
        retlist.append(row['category_id'])
    return retlist

def __expand_to_sub_categories__(category_id):
    sql = 'select distinct id from jd_category where id like "%s-%%"' %category_id
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


if __name__ == "__main__":
    argv = sys.argv

    M = N = 1
    if len(argv) == 2:
        print 'Error in arguments'
    elif len(argv) == 3:
        try:
            M = int(argv[1])
            N = int(argv[2])
        except:
            print 'Error in arguments'

    data_task = Jd_List_DataTask()
    data_task.configTask(is_daily=False, interval_hours=1, sleep_time=0.5)
    data_task.doTask(M,N)


