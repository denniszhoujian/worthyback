# encoding: utf-8

from process_class import WorthyProcessBase
from worthy_analytics import promo_item_trans, final_discount

func_list = [
    promo_item_trans.processItemPromo,      # 90 secs
    promo_item_trans.process_promo_detail,  # 10 secs
    promo_item_trans.process_gift_value,    # 2 secs
    final_discount.match_discounts,         # 25 secs
]

if __name__ == '__main__':
    wp = WorthyProcessBase(
        function_list=func_list,
        is_daily=False,
        start_hour=0, # no use
        interval_secs=600,
        min_sleep=120 # 2 mins
    )
    wp.run_tasks_repeated()

