# encoding: utf-8

import sys
import dbhelper
import time
from task_class import DataTask
import jd_detail_crawler
import mylog
import timeHelper

reload(sys)
sys.setdefaultencoding('utf8')

mylog.configLogging('property_task')

class Jd_Property_DataTask(DataTask):

    def __init__(self,job_name):
        self.job_name = job_name

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
    def __task_order__(self,task_id):
        return jd_detail_crawler.crawl_detail_all(task_id)

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

    data_task = Jd_Property_DataTask(job_name="JD_PROPERTY_CRAWLER")
    data_task.configTask(is_daily=False,interval_hours=24*30,sleep_time=0.2,repeat_interval=24,record_task_complete=True)
    data_task.doTask(M,N)


