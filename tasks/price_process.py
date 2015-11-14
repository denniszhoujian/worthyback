# encoding: utf-8

from datasys import timeHelper
import time
import worthy_analytics.base_price
from process_class import WorthyProcessBase


func_list = [
    worthy_analytics.base_price.calculate_price_table, # normally within 2 mins
]

if __name__ == "__main__":


    # wp = WorthyProcessBase(
    #     function_list=func_list,
    #     is_daily=False,
    #     start_hour=0,
    #     interval_secs=900,
    #     min_sleep=600
    # )
    #
    # wp.run_tasks_repeated()
    pass

