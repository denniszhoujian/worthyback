# encoding : utf-8

from datasys import crawler_helper,dbhelper
import rows_helper
import datamining_config
from collections import OrderedDict
import time


def _get_ordered_array(non_ordered_array, order_key_col):
    a = non_ordered_array
    a.sort(cmp=lambda x,y:cmp(x[order_key_col],y[order_key_col]))

def _find_small_to_large_index_halfwaymethod(val, ordedered_list):
    # list small to large, already ordered
    val = float(val)
    total_num = len(ordedered_list)
    idx = total_num//2
    min = 0
    max = total_num-1
    iters = 0
    while idx<max and idx>=min and iters<=total_num:
        if val>=ordedered_list[idx]:
            min = idx
            idx = int((idx + max) / 2.0)
        else:
            max = idx
            idx = int((min + idx) / 2.0)
        iters += 1
    # if iters >= total_num -1:
    #     print "ERROROROROROR"
    return idx

# alist = [
#     2,
#     3,
#     4,
#     5.5,
#     6.5,
#     7.8,
#     7.9,
#     8.0,
#     8.1,
#     9,
#     10,
#     12,
#     16.5,
# ]
#
# for i in range(0,10):
#     print _find_small_to_large_index_halfwaymethod(alist[i]+0.01,alist)


def _getPercentileGreaterThan(my_value, ordered_rows, order_key_col):
    if my_value is None:
        return None
    my_value = float(my_value)
    sum = 0
    olist = []
    for row in ordered_rows:
        try:
            olist.append(float(row[order_key_col]))
            sum += 1
        except Exception as e:
            print "error in get percentile loop: %s" %e

    if sum < datamining_config.MIN_SKU_NUM_PER_CATEGORY_SO_STATISTICALLY_SIGNIFICANT:
        return None

    idx = _find_small_to_large_index_halfwaymethod(my_value,olist)
    MIN = 0.0001
    #
    # sum = 0
    # idx = 0
    # for item in ordered_rows:
    #     # print "myval = %s\t this = %s" %(my_value,item[order_key_col] )
    #     if item[order_key_col] is None:
    #         continue
    #     sum += 1.00
    #     if my_value > float(item[order_key_col]):
    #         idx += 1.00
    # # print "idx = %s\tsum=%s\n\n" %(idx,sum)

    return (idx+MIN)/(sum+MIN)


def calculatePercentile():
    """
    (1) load data
    (2) hash by key: category_id, ordered dict
    (3) for each item, find it's category_id array, got it's pos and percentile
    (4) store results in db
    :return:
    """

    t1 = time.time()

    # STEP (1)
    print "step 1/4: reading data from rating_score_latest"
    sql = '''
    select * from jd_analytic_rating_score_latest
    where
    rating_score is NOT NULL and
    comment_count is not NULL AND comment_count >= %s
    -- and category_id like "670-729-%%" order by comment_count DESC
    order by category_id
    -- limit 1000
    ''' %datamining_config.MIN_SKU_NUM_PER_CATEGORY_SO_STATISTICALLY_SIGNIFICANT

    retrows = dbhelper.executeSqlRead(sql)
    t2 = time.time()
    print "Done, rows read: %s, seconds used: %0.1f" %(len(retrows), t2-t1)

    # STEP (2)

    print "step 2/4: sorting category scores..."
    print ""

    key_col = 'rating_score'

    tdict = rows_helper.transform_retrows_to_hashed_arrays(retrows, key_col_name='category_id')
    odict = {}
    for cat in tdict:
        array = tdict[cat]
        _get_ordered_array(array, key_col)
        odict[cat] = array
    t3 = time.time()
    print "Done, ordered_dict generated, num of keys = %s, time used = %0.1f" %(len(odict),t3-t2)
    print ""

    # STEP (3)

    print "step 3/4: calculate rating percentile for each sku..."
    #sku_dict = rows_helper.transform_retrows_to_dict(retrows, key_col_name='sku_id')
    for row in retrows:
        catid = row['category_id']
        myval = row[key_col]
        pt = _getPercentileGreaterThan(myval,odict[catid],key_col)
        row['percentile_'+key_col] = pt
        row['sample_num'] = len(odict[catid]) if odict[catid] is not None else 0
        # print "myval: %s\tpt: %s" %(myval,pt)
    t4 = time.time()
    print "Done, using seconds: %0.1f" %(t4-t3)
    print ""

    # Step (4)
    print 'step 4/4: storing results in db...'
    # for item in retrows:
    #     for key in item:
    #         print key
    #     break

    sql_cb = '''
    CREATE TABLE jd_analytic_rating_percentile_latest (
          sku_id bigint(20) NOT NULL,
          comment_count int(11) NOT NULL,
          this_update_time datetime NOT NULL,
          rating_score float NOT NULL,
          category_id varchar(255) NOT NULL,
          rating_sample_num int(11) DEFAULT 0,
          percentile_rating_score float DEFAULT NULL,
          PRIMARY KEY (sku_id),
          KEY skuid (sku_id)
          -- KEY cat_score (rating_score,category_id),
          -- KEY score (rating_score),
          -- KEY category (category_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8

    '''
    vlist = rows_helper.transform_retrows_arrayofdicts_to_arrayoftuples(retrows)
    ret = crawler_helper.persist_db_history_and_lastest_empty_first(
        table_name='jd_analytic_rating_percentile',
        num_cols=len(vlist[0]),
        value_list=vlist,
        is_many=True,
        need_history=False,
        sql_create_table=sql_cb,
    )
    t5 = time.time()
    print "Done, rows affected: %s, time used: %0.1f" %(ret, t5-t4)
    print ""
    return ret


def calculateSkuRatingScores():

    sql_cb = '''
        CREATE TABLE jd_analytic_rating_score_latest (
          sku_id bigint(20) NOT NULL,
          comment_count int(11) NOT NULL,
          rating_score float DEFAULT NULL,
          category_id varchar(255) NOT NULL,
          this_update_time datetime NOT NULL,
          PRIMARY KEY (sku_id)
          -- KEY skuid (sku_id),
          -- KEY cat_score (rating_score,category_id),
          -- KEY score (rating_score),
          -- KEY category (category_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        '''

    sql = '''
        select

        skuid as sku_id,
        CommentCount,
        ((a.Score1Count)*1.0+(a.Score2Count)*2.0+(a.Score3Count)*3.0+(a.Score4Count)*4.0+(a.Score5Count)*5.0)/a.CommentCount as rating_score,
        category_id,
        CURRENT_TIMESTAMP() as this_update_time

        from

        jd_item_comment_count_latest a
        left join
        jd_item_category b
        on a.SkuId = b.sku_id

        where a.CommentCount is not null and a.CommentCount >= %s

        ''' %(datamining_config.MIN_COMMENT_NUM_SO_RATING_SCORE_STATISTICALLY_SIGNIFICANT)

    retrows = dbhelper.executeSqlRead2(sql,is_dirty=True)

    ret = crawler_helper.persist_db_history_and_lastest_empty_first(
        table_name='jd_analytic_rating_score',
        num_cols=len(retrows[0]),
        value_list=retrows,
        need_history=False,
        is_many=True,
        sql_create_table=sql_cb,
    )

    return ret


if __name__ == '__main__':
    t1 = time.time()
    print calculateSkuRatingScores()
    t2 = time.time()
    print "####: %s" %(t2-t1)

    print calculatePercentile()