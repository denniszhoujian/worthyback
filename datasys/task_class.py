# encoding: utf-8

import sys
import time
import logging

from datasys import timeHelper
import dbhelper


reload(sys)
sys.setdefaultencoding('utf8')

class DataTask():

    job_name = ""
    SLEEP_TIME = 0.5

    # VIRTUAL
    def __load_all_tasks__(self):
        pass

    # VIRTUAL
    def __task_order__(self,task_id):
        pass

    def __record_task_complete__(self, task_id):
        sql = 'insert into task_status(job_name,task_id,update_time) values("%s","%s","%s")' %(self.job_name,task_id,
                                                                                               timeHelper.getNowLong())
        affected_rows = dbhelper.executeSqlWrite1(sql)
        return affected_rows

    def __get_task_already_done__(self):
        sql = 'select task_id from task_status where job_name="%s" and update_time>="%s 0:00:00"' %(self.job_name,
                                                                                                timeHelper.getNow())
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

        for cat_id in task_list:
            ret = self.__task_order__(cat_id)
            time.sleep(self.SLEEP_TIME)
            logging.info('return: %s' %ret)
            if ret['status'] == 0:
                self.__record_task_complete__(cat_id)
                logging.info('recorded task complete: %s' %cat_id)
            else:
                logging.error('TASK EXECUTION FAILED. TASK_ID = %s' %cat_id)
                is_success = 0
        return is_success


    def doTask(self,M=1,N=1):
        while True:
            t1 = time.time()
            self.doTaskOnce(M,N)
            t2 = time.time()
            remaining = timeHelper.getTimeLeftTillTomorrow()
            logging.info('='*80)
            logging.info('Finished crawling, using time: %s seconds' %(t2-t1))
            logging.info('Now sleeping for %s seconds till tomorrow' %(remaining))
            logging.info('='*80)
            time.sleep(remaining)


if __name__ == "__main__":
    argv = sys.argv
    la = len(argv)

    # VIRTUAL, DO NOTHING HERE
