# encoding: utf-8

import sys
import time
import timeHelper
import dbhelper
import logging
import copy

reload(sys)
sys.setdefaultencoding('utf8')

TASK_TIMES_OF_RETRY_ON_ERROR = 3
TASK_RETRY_SLEEP_TIME = 5
ITERATED_TASK_ERROR_INTERVAL = 600

def abstract():
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')

class DataTask():

    job_name = ""
    is_daily = True
    interval_hours = 24
    SLEEP_TIME = 0.5
    group_num = 1

    def __init__(self):
        self.job_name = self.__class__

    def __load_all_tasks__(self):abstract()

    def __task_order__(self,task_id):abstract()

    def configTask(self, is_daily, interval_hours, sleep_time,group_num=1):
        self.is_daily = is_daily
        self.interval_hours = interval_hours
        self.SLEEP_TIME = sleep_time
        self.group_num=group_num

    def __record_task_complete__(self, task_list):
        vlist = []
        ut = timeHelper.getNowLong()
        for item in task_list:
            tp = (self.job_name,item,ut)
            vlist.append(tp)
        sql = 'insert into task_status(job_name,task_id,update_time) values(%s,%s,%s)'
        affected_rows = dbhelper.executeSqlWriteMany(sql,vlist)
        return affected_rows

    def __get_task_already_done__(self):
        if self.is_daily:
            sql = 'select task_id from task_status where job_name="%s" and update_time>="%s 0:00:00"' %(self.job_name,timeHelper.getNow())
        else:
            stime = timeHelper.getTimeAheadOfNowHours(self.interval_hours)
            sql = 'select task_id from task_status where job_name="%s" and update_time>="%s 0:00:00"' %(self.job_name,stime)
        retrows = dbhelper.executeSqlRead(sql)
        catlist = []
        for row in retrows:
            catlist.append(row['task_id'])
        return catlist

    def __remove_completed_tasks__(self,task_list):
        done_list = self.__get_task_already_done__()
        return list(set(task_list)-set(done_list))

    def __load_thread_tasks__(self,M,N):
        all_tasks = self.__load_all_tasks__()
        dedup_tasks = self.__remove_completed_tasks__(all_tasks)
        thread_tasks = []
        for i in xrange(len(dedup_tasks)):
            if i % N == (M-1):
                thread_tasks.append(dedup_tasks[i])
        return thread_tasks

    def doTaskOnce(self,M=1,N=1):
        task_list = self.__load_thread_tasks__(M,N)
        logging.info('Job_name = %s\tTotal tasks: %s' %(self.job_name,len(task_list)))
        is_success = 1
        glist = []
        gsize = self.group_num
        accumulated_task_num = 0
        all_task_num = len(task_list)
        iter = 0
        for cat_id in task_list:
            iter += 1
            group_task_list = []
            glist.append(cat_id)
            accumulated_task_num += 1

            if accumulated_task_num < gsize and iter < all_task_num:
                continue
            else:
                accumulated_task_num = 0
                # print glist
                for item in glist:
                    group_task_list.append(item)
                glist = []

            # print 'debug'
            # print len(group_task_list)
            # print group_task_list

            tries = 0
            is_task_success = 0
            while tries < TASK_TIMES_OF_RETRY_ON_ERROR:
                tries += 1
                try:
                    if gsize == 1:
                        ret = self.__task_order__(cat_id)
                    else:
                        ret = self.__task_order__(group_task_list)
                    time.sleep(self.SLEEP_TIME)
                    logging.info('return: %s' %ret)
                    if ret['status'] == 0:
                        self.__record_task_complete__(group_task_list)
                        logging.info('recorded task complete: %s' %group_task_list)
                        is_task_success = 1
                    else:
                        logging.error('TASK EXECUTION FAILED. TASK_ID = %s' %group_task_list)
                        is_task_success = 0
                    break
                except Exception as e:
                    logging.error('Task failed, task_id = %s'%group_task_list)
                    logging.error(e)
                    time.sleep(TASK_RETRY_SLEEP_TIME)
                    continue
            if is_task_success == 0:
                is_success = 0
        return is_success

    def doTask(self,M=1,N=1):
        while True:
            print 'start job - %s' %timeHelper.getNowLong()
            t1 = time.time()
            is_success = self.doTaskOnce(M,N)
            t2 = time.time()
            remaining = timeHelper.getTimeLeftTillTomorrow() if is_success==1 else ITERATED_TASK_ERROR_INTERVAL
            logging.info('='*80)
            logging.info('Finished crawling, using time: %s seconds' %(t2-t1))
            logging.info('Has Errors? %s' %('NO' if is_success==1 else 'YES'))
            logging.info('Now sleeping for %s seconds for next run' %(remaining))
            logging.info('='*80)
            time.sleep(remaining)


if __name__ == "__main__":
    argv = sys.argv
    la = len(argv)

    # VIRTUAL, DO NOTHING HERE
