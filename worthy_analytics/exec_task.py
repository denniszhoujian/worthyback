# encoding: utf-8

from datasys import timeHelper
import time
import rating_diff,base_price,base_rating


task_func_list = [
    base_price.calculate_price_table,
    base_rating.calculate_base_rating_for_categories,
    rating_diff.calculate_rating_diff,

]



def run_tasks_once():
    print "-" * 80
    print "Function list:"
    for item in task_func_list:
        print item
    print "-" * 80
    has_error = False
    has_error_anywhere = False
    for func in task_func_list:
        has_error = False
        print "*" * 60
        print "now running func: %s" %(func)
        t1 = time.time()
        try:

            ret = func()
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> func %s returning value: %s >>>>>>>>>>>>>>>>>>>>>>" %(func, ret)

        except Exception as e:
            print "ERROR GREP LINE"
            print e
            has_error = True
            has_error_anywhere = True
        t2 = time.time()
        print "completed running func %s, using seconds = %s, has_error = %s \n" %(func, t2-t1, has_error)

    return has_error_anywhere


def run_tasks_repeated():
    while True:
        has_error = False
        print "\n\n\nJob start at %s" %timeHelper.getNowLong()
        try:
            t1 = time.time()
            has_error  = run_tasks_once()
            t2 = time.time()
            print "RUN-ONCE TOTALLY TAKING TIME: %s seconds" %(t2-t1)
            print "-" * 60
        except Exception as e:
            print "ERROR GREP LINE"
            print e
            has_error = True
        remaining = timeHelper.getTimeLeftTillTomorrow()

        print "HAS ERROR TODAY? %s" %has_error
        print "Sleep to tomorrow: hours left = %s" %(remaining/3600)

        time.sleep(remaining)
        ###


if __name__ == "__main__":
    run_tasks_repeated()

