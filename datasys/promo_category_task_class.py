# encoding: utf-8

import sys
import dbhelper
import time
from task_class import DataTask
import jd_api_crawler
import mylog
import category_helper

reload(sys)
sys.setdefaultencoding('utf8')

mylog.configLogging('promo_category_task')

class Jd_Promo_Category_DataTask(DataTask):

     # VIRTUAL
    def __load_all_tasks__(self):
        return category_helper.load_all_white_sub_categories()

    # VIRTUAL
    def __task_order__(self,task_id):
        return jd_api_crawler.crawl_category_promo(task_id)

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

    data_task = Jd_Promo_Category_DataTask()
    data_task.configTask(is_daily=False,interval_hours=12,sleep_time=2)
    data_task.doTask(M,N)


