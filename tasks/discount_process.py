# encoding: utf-8

from process_class import WorthyProcessBase
from worthy_analytics import promo_item_trans, worthy_mix, base_price
import task_logging
from indexer import rotate_index


# pipeline
func_list = [
    base_price.calculate_min_max_price,     # 150 secs
    promo_item_trans.processItemPromo,      # 15 secs
    promo_item_trans.process_promo_detail,  # 25 secs
    promo_item_trans.process_gift_value,    # 1 secs
    worthy_mix.generate_worthy_mix_main,    # 400 secs
    rotate_index.execute_rotate_index,      # 10 secs
    # rotate_index.flush_memcache_content,    # 5 secs
    rotate_index.re_cache,                  # 10 secs
]

if __name__ == '__main__':

    task_logging.configLogging('analytic_discount')

    wp = WorthyProcessBase(
        function_list=func_list,
        is_daily=False,
        start_hour=0, # no use
        interval_secs=3600*1.5, # 4 hours
        min_sleep=1200 # 20 mins
    )
    wp.run_tasks_repeated()

