# encoding: utf-8

from datasys import timeHelper
import time

class WorthyProcessBase:

    task_func_list = None
    #start at 3:00AM
    START_HOUR = 3
    is_daily = True
    interval_seconds = 86400
    min_sleep = 600

    def __init__(self,function_list,is_daily,start_hour,interval_secs,min_sleep):
        self.task_func_list = function_list
        self.is_daily = is_daily
        self.START_HOUR = start_hour
        self.interval_seconds = interval_secs
        self.min_sleep = min_sleep

    def run_tasks_once(self):
        print "=" * 120
        print "Function list:"
        print "=" * 120
        for item in self.task_func_list:
            print '\t%s' %item
        print '=' * 120
        print
        print
        has_error = False
        has_error_anywhere = False
        for func in self.task_func_list:
            has_error = False
            print
            print "*" * 120
            print "now running func: %s" %(func)
            print "*" * 120
            print
            t1 = time.time()
            try:

                ret = func()
                print "\t##### func %s returning value: %s ######" %(func, ret)

            except Exception as e:
                print "ERROR GREP LINE >>>>>>>>" * 5
                print e
                has_error = True
                has_error_anywhere = True
            t2 = time.time()
            print "\tcompleted running func %s, using seconds = %s, has_error = %s \n" %(func, t2-t1, has_error)

        return has_error_anywhere


    def run_tasks_repeated(self):

        while True:
            has_error = False
            print "\n\n\nJob start at %s" %timeHelper.getNowLong()
            t1 = time.time()
            try:
                has_error  = self.run_tasks_once()
            except Exception as e:
                print "ERROR GREP LINE >>>>>>" * 5
                print e
                has_error = True

            print "HAS ERROR TODAY? %s" %has_error

            t2 = time.time()
            print "RUN-ONCE TOTALLY TAKING TIME: %s seconds" %(t2-t1)
            print "-" * 60


            if self.is_daily:
                remaining = timeHelper.getTimeLeftTillTomorrow() + self.START_HOUR*3600 + 10
                print "Sleep to tomorrow, at %s:00:00 hour: hours left = %s" %(self.START_HOUR,remaining/3600)
            else:
                inter = self.interval_seconds - int(t2-t1)
                if inter < 0:
                    inter = 0
                remaining = inter + self.START_HOUR*3600 + 10
                print "Sleep to fill interval, seconds left = %s" %(remaining)

            if remaining < self.min_sleep:
                remaining = self.min_sleep

            time.sleep(remaining)
            ### END ###



