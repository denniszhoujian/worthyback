# encoding: utf-8

from process_class import WorthyProcessBase
from worthy_analytics import promo_item_trans, worthy_mix, base_price
import task_logging
from indexer import rotate_index
from notification import history_lowest
from datasys import price_task_class

# pipeline
func_list = [

    # price_task_class.update_price,          # 900 secs now          # 400 secs originally

    base_price.calculate_min_max_price,     # 25 secs on monster    # 50 secs on mba
    promo_item_trans.processItemPromo,      # 5 secs on monster     # 15 secs on mba
    promo_item_trans.process_promo_detail,  # 5 secs on monster     # 25 secs
    promo_item_trans.process_gift_value,    # << 1 secs
    worthy_mix.generate_worthy_mix_main,    # 180 secs on monster   # 140 secs on mba
    rotate_index.execute_rotate_index,      # 13 secs on monster    # 10 secs on mba
    rotate_index.flush_memcache_content,    # << 1  secs
    rotate_index.re_cache,                  # 35 secs on monster    # 10 secs on mba

    # notification
    history_lowest.update_history_lowest_store,     # << 1 secs
    history_lowest.temp_sendSMS,                    # 2 secs
]

if __name__ == '__main__':

    task_logging.configLogging('analytic_discount')

    wp = WorthyProcessBase(
        function_list=func_list,
        is_daily=False,
        start_hour=0, # no use
        interval_secs=600, # 4 hours
        min_sleep=60 # 20 mins
    )
    wp.run_tasks_repeated()

