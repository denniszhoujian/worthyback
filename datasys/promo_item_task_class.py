# encoding: utf-8

import sys
import dbhelper
import time
from task_class import DataTask
import jd_api_crawler
import mylog

reload(sys)
sys.setdefaultencoding('utf8')

class Jd_Promo_item_DataTask(DataTask):

     # VIRTUAL
    def __load_all_tasks__(self):
        sql = 'select distinct sku_id from jd_item_category'
        retrows = dbhelper.executeSqlRead2(sql)
        sku_list = []
        for row in retrows:
            sku_list.append(row[0])
        return sku_list

    # VIRTUAL
    def __task_order__(self,task_id):
        return jd_api_crawler.crawl_item_promo(task_id)

#
# ==================================================================================
#

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

    mylog.configLogging('promo_item_task_%s_%s' %(M,N))

    data_task = Jd_Promo_item_DataTask()
    data_task.configTask(is_daily=False,interval_hours=0,sleep_time=0.1)
    data_task.doTask(M,N)


