# encoding: utf-8

from process_class import WorthyProcessBase
from worthy_analytics import promo_item_trans, worthy_mix, base_price
import task_logging
from indexer import rotate_index


# pipeline
func_list = [
    base_price.calculate_min_max_price,     # 90 secs
    promo_item_trans.processItemPromo,      # 90 secs
    promo_item_trans.process_promo_detail,  # 10 secs
    promo_item_trans.process_gift_value,    # 2 secs
    worthy_mix.generate_worthy_mix_main,    # 300 secs
    rotate_index.execute_rotate_index(),    # 5 secs
    rotate_index.flush_memcache_content(),  # 1 secs
    rotate_index.re_cache(),                # ? secs
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

