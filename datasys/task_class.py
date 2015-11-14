# encoding: utf-8

import sys
import time
import timeHelper
import dbhelper
import logging
import copy

reload(sys)
sys.setdefaultencoding('utf8')

TASK_TIMES_OF_RETRY_ON_ERROR = 1    # WAS 3
TASK_RETRY_SLEEP_TIME = 5
# ITERATED_TASK_ERROR_INTERVAL = 600


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
    num_all = 1
    num_remaining = 0

    def __init__(self):
        self.job_name = self.__class__

    def __load_all_tasks__(self):abstract()

    def __task_order__(self,task_id):abstract()

    def configTask(self, is_daily, interval_hours, sleep_time,group_num=1):
        self.is_daily = is_daily
        self.interval_hours = interval_hours
        self.SLEEP_TIME = sleep_time
        self.group_num=group_num

    def __make_string_array__ (self, plist):
        vlist = []
        for item in plist:
            vlist.append("%s" %item)
        return vlist

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
            sql = 'select task_id from task_status where job_name="%s" and update_time>="%s 0:00:00" group by task_id' %(self.job_name,timeHelper.getNow())
        else:
            stime = timeHelper.getTimeAheadOfNowHours(self.interval_hours,format='%Y-%m-%d %H:%M:%S')
            sql = 'select task_id from task_status where job_name="%s" and update_time>="%s" group by task_id' %(self.job_name,stime)
        # print sql
        retrows = dbhelper.executeSqlRead(sql,is_dirty=True)
        catlist = []
        for row in retrows:
            catlist.append("%s" %row['task_id'])
        logging.info("Task already done: %s" %len(catlist))
        print("Task already done: %s" %len(catlist))
        return catlist

    def __remove_completed_tasks__(self,task_list):
        done_list = self.__get_task_already_done__()
        done_list = self.__make_string_array__(done_list)
        # print len(done_list)
        # print len(set(done_list))
        # print len(set(task_list))
        ret = list(set(task_list) - set(done_list))
        # print len(ret)
        return ret

    def __load_thread_tasks__(self,M,N):
        all_tasks = self.__load_all_tasks__()
        all_tasks = self.__make_string_array__(all_tasks)
        self.num_all = len(all_tasks)*1.0/N + 0.00001
        logging.info("All tasks: %s" %len(all_tasks))
        print("All tasks: %s" %len(all_tasks))

        dedup_tasks = self.__remove_completed_tasks__(all_tasks)
        # self.num_remaining = len(dedup_tasks)*1.0
        thread_tasks = []
        for i in xrange(len(dedup_tasks)):
            if i % N == (M-1):
                thread_tasks.append(dedup_tasks[i])

        self.num_remaining = len(thread_tasks)*1.0

        logging.info("Remaining tasks: %s" %len(dedup_tasks))
        logging.info("Thread tasks: %s" %len(thread_tasks))
        logging.info("Tasks completed: %.0f%%" %((self.num_all-self.num_remaining)/self.num_all*100.0)  )

        print("Remaining tasks: %s" %len(dedup_tasks))
        print("Thread tasks: %s" %len(thread_tasks))
        print("Tasks completed: %.0f%%" %((self.num_all-self.num_remaining)/self.num_all*100.0)  )
        print("="*80)

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
        t_init = time.time()
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
            last_complete_percent = (self.num_all-self.num_remaining)/self.num_all*100.0
            while tries < TASK_TIMES_OF_RETRY_ON_ERROR:
                tries += 1
                try:
                    if gsize == 1:
                        ret = self.__task_order__(cat_id)
                    else:
                        ret = self.__task_order__(group_task_list)

                    logging.debug('return: %s' %ret)

                    if ret['status'] == 0:
                        self.__record_task_complete__(group_task_list)
                        #logging.info('recorded task complete: %s' %group_task_list)
                        is_task_success = 1
                    else:
                        logging.error('TASK EXECUTION FAILED. TASK_ID = %s' %group_task_list)
                        is_task_success = 0

                    # self.num_remaining -= 1.0
                    self.num_remaining -= len(group_task_list)
                    complete_percent = (self.num_all-self.num_remaining)/self.num_all*100.0
                    if (complete_percent-last_complete_percent) >= 9.9999:
                        t_now = time.time()
                        logging.info("Tasks completed: %.1f%%, ellapsed seconds: %s" %(complete_percent,int(t_now-t_init)))
                        last_complete_percent = complete_percent

                    logging.debug("Tasks completed: %.1f%%" %complete_percent)
                    time.sleep(self.SLEEP_TIME)
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
            retry = 0
            print 'start job - %s' %timeHelper.getNowLong()
            t1 = time.time()
            is_success = self.doTaskOnce(M,N)
            t2 = time.time()

            remaining = 600
            if self.is_daily:
                remaining = timeHelper.getTimeLeftTillTomorrow()
            else:
                remaining = int(self.interval_hours * 3600 - (t2-t1))
                if remaining < 0:
                    remaining = 0
            remaining += 10
            logging.info('='*80)
            logging.info('Finished crawling, using time: %s seconds' %(t2-t1))
            logging.info('Has Errors? %s' %('NO' if is_success==1 else 'YES'))
            logging.info('Now sleeping for %s seconds for next run (%.1f hours)' %(remaining,remaining/3600))
            logging.info('='*80)
            time.sleep(remaining)

