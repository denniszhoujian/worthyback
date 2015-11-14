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

mylog.configLogging('comment_stats_task')

class Jd_Comment_Stats_DataTask(DataTask):

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
        return jd_api_crawler.crawl_sku_comment_count(task_id)

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

    data_task = Jd_Comment_Stats_DataTask()
    data_task.configTask(is_daily=True,interval_hours=24,sleep_time=0.2,group_num=50)
    data_task.doTask(M,N)


