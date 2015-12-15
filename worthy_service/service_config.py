# encoding: utf-8

########################################################################
#### SERVCIE
########################################################################

SKU_LIST_CACHE_TIME_OUT = 3600*2 # seconds
SKU_LIST_FRAME_SIZE = 30
SKU_LIST_MIN_PRICE_FOR_EXPENSIVE = 800 #CNY
SKU_LIST_MAX_ALLOWED_PRICE = 30000 #CNY
SKU_LIST_MIN_ALLOWED_PRICE = 20.0 #CNY
SKU_LIST_IF_USE_REAL_TIME_PRICE = False
SKU_LIST_MIN_ALLOWED_WORTHY_VALUE = 0.90
SKU_LIST_APP_WORTHY_RECENCY_HOURS = 28

SKU_LIST_MAX_RECALL_NUM = 1000
SKU_LIST_RERANK_TOP_NUM = 300

SKU_INDEX_WEIGHT_DICT = {
    'title': 8,
    'category_name':20,
    'catalog_name':4,
    'name_deduction':10,
    'name_discount':10,
    'name_lowest':10,
    'property_text':4,
    'category_text':4,
}

QUERY_HISTORY_MAX_NUM = 15
CATALOG_HISTORY_MAX_NUM = 6

CATEGORY_INDICATOR_MAX_NUM = 10
PROPERTY_INDICATOR_MAX_NUM = 20

PROPERTY_KEY_BLACK_WORD_LIST = [
    '保质期',
    '其他',
    '其他特征',
]