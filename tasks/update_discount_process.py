# encoding: utf-8

from process_class import WorthyProcessBase
from worthy_analytics import promo_item_trans

func_list = [
    promo_item_trans.update_promo_results,      # seen 1 sec

]

if __name__ == '__main__':
    wp = WorthyProcessBase(
        function_list=func_list,
        is_daily=False,
        start_hour=0, # no use
        interval_secs=0,
        min_sleep=60 # 10 mins
    )
    wp.run_tasks_repeated()

