# encoding: utf-8

from datasys import timeHelper
import time
import worthy_analytics.rating_diff, worthy_analytics.base_price, worthy_analytics.base_rating, worthy_analytics.promo_item_trans
from worthy_analytics import rating_percentile
from process_class import WorthyProcessBase


func_list = [
    # worthy_analytics.base_rating.calculate_base_rating_for_categories,
    # worthy_analytics.rating_diff.calculate_rating_diff,
    rating_percentile.calculateSkuRatingScores,
    rating_percentile.calculatePercentile,
]

if __name__ == "__main__":

    wp = WorthyProcessBase(
        function_list=func_list,
        is_daily=True,
        start_hour=8,
        interval_secs=900, #no-use
        min_sleep=600
    )

    wp.run_tasks_repeated()
    