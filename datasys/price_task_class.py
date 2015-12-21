# encoding: utf-8

import sys
import dbhelper
import time
from task_class import DataTask
import jd_api_crawler
import mylog
import timeHelper

reload(sys)
sys.setdefaultencoding('utf8')

class Jd_Price_Task(DataTask):

     # VIRTUAL
    def __load_all_tasks__(self):
        daysago3 = timeHelper.getTimeAheadOfNowDays(3)
        sql = 'select distinct sku_id from jd_item_dynamic_latest where update_date >= "%s"' %daysago3
        retrows = dbhelper.executeSqlRead2(sql, is_dirty=True)
        sku_list = []
        for row in retrows:
            sku_list.append(row[0])
        return sku_list

    # VIRTUAL
    def __task_order__(self,task_list):
        return jd_api_crawler.crawl_sku_price(task_list,self.SLEEP_TIME)

def update_price():
    M = N = 1
    mylog.configLogging('price_task_%s_%s' %(M,N))

    data_task = Jd_Price_Task()
    data_task.configTask(is_daily=False,interval_hours=0,sleep_time=0.1, group_num=2000)
    data_task.doTaskOnce(M,N)

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

    mylog.configLogging('price_task_%s_%s' %(M,N))

    data_task = Jd_Price_Task()
    data_task.configTask(is_daily=False,interval_hours=0,sleep_time=0.1, group_num=2000)
    data_task.doTask(M,N)


