# encoding: utf-8


# RECENCY CONFIGURATIONS
PRICE_RECENCY_HOURS = 12
PROMO_ITEM_RECENCY_HOURS = 12

# RATING CONFIG
MIN_SKU_NUM_PER_CATEGORY_SO_STATISTICALLY_SIGNIFICANT = 20
MIN_COMMENT_NUM_SO_RATING_SCORE_STATISTICALLY_SIGNIFICANT = 20

# MIN_PRICE REACHED CONFIG
SKU_MIN_PRICE_REACHED_MINIMUM_REQUIRED_DISCOUNT_RATE = 0.90

# WEIGHT CONFIG
MAX_REACH_NUM_FOR_DISCOUNT = 3
DISCOUNT_REACH_NUM_POWER_BASE = 1.6
MAX_GIFT_DISCOUNT = 0.5

##### For any score_matrix, key MUST be ordered ASC
RATING_PERCENTILE_SCORE_MATRIX = {
    0.5:1.0,
    0.7:0.95,
    0.8:0.90,
    0.9:0.80,
    0.95:0.95,
}
MIN_PRICE_REACHED_SCORE_MATRIX = {
    1:1.0,
    2:0.8,  # history low-est is taken as an additional 20% discount :)
}

# RANK CONFIGURATIONS

col_worthyvalue_weight_dict_1 = {
            'discount_rate': 1.0,
            'deduction_final_score': 1.0,
            'discount': 0.75,
            'rf_ratio': 0.6,
            'gift_ratio': 0.1,
            'rating_score_diff': 1.0,
            'min_price_reached': 1.0,
        }


# if __name__ == "__main__":
#     import worthy_mix
#     print worthy_mix._calculate_ladder_score(0.83,RATING_PERCENTILE_SCORE_MATRIX)

