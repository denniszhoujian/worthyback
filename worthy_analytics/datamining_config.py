# encoding: utf-8


# RECENCY CONFIGURATIONS
PRICE_RECENCY_HOURS = 12
PROMO_ITEM_RECENCY_HOURS = 12

# RATING CONFIG
MIN_SKU_NUM_PER_CATEGORY_SO_STATISTICALLY_SIGNIFICANT = 20
MIN_COMMENT_NUM_SO_RATING_SCORE_STATISTICALLY_SIGNIFICANT = 20


# WEIGHT CONFIG
MAX_REACH_NUM_FOR_DISCOUNT = 3
DISCOUNT_REACH_NUM_POWER_BASE = 1.6
MAX_GIFT_DISCOUNT = 0.5


# RANK CONFIGURATIONS

col_worthyvalue_weight_dict_1 = {
            'discount_rate': 1.0,
            # 'max_deduction_ratio': 1.0,
            # 'deduction_score': 0.8,
            'deduction_final_score': 1.0,
            'discount': 0.75,
            'rf_ratio': 0.6,
            'gift_ratio': 0.3,
            'rating_score_diff': 0.2,
        }
