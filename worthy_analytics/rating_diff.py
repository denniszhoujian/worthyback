# encoding: utf-8

from datasys import dbhelper, timeHelper
import time

def calculate_rating_diff() :

    sql = '''
        replace into jd_analytic_item_rating_diff

        select

        a.SkuId,
        '%s' as dt,
        c.category_id,
        d.name as category_name,
        a.CommentCount,
        c.sample_count as category_sample_count,

        ((a.Score1Count)*1.0+(a.Score2Count)*2.0+(a.Score3Count)*3.0+(a.Score4Count)*4.0+(a.Score5Count)*5.0)/a.CommentCount as rating_score,
        c.rating_score as category_rating_score,
         ((a.Score1Count)*1.0+(a.Score2Count)*2.0+(a.Score3Count)*3.0+(a.Score4Count)*4.0+(a.Score5Count)*5.0)/a.CommentCount*1.0/c.rating_score as rating_score_diff,

        (a.Score4Count+a.Score5Count)/a.CommentCount as rate_good,
        c.rate_good as category_rate_good,
        Format(((a.Score4Count+a.Score5Count)/a.CommentCount - c.rate_good)*100/c.rate_good,1) as rate_good_diff,

        (a.Score1Count+a.Score2Count)/a.CommentCount as rate_bad,
        c.rate_bad as category_rate_bad,
        Format(((a.Score1Count+a.Score2Count)/a.CommentCount - c.rate_bad)*100/c.rate_bad,1) as rate_bad_diff,

        a.Score1Count/a.CommentCount as rate_1,
        c.rate_1 as category_rate_1,
        Format((a.Score1Count/a.CommentCount - c.rate_1)*100/c.rate_1,1) as rate_1_diff,

        a.Score2Count/a.CommentCount as rate_2,
        c.rate_2 as category_rate_2,
        Format((a.Score2Count/a.CommentCount - c.rate_2)*100/c.rate_2,1) as rate_2_diff,

        a.Score3Count/a.CommentCount as rate_3,
        c.rate_3 as category_rate_3,
        Format((a.Score3Count/a.CommentCount - c.rate_3)*100/c.rate_3,1) as rate_3_diff,

        a.Score4Count/a.CommentCount as rate_4,
        c.rate_4 as category_rate_4,
        Format((a.Score4Count/a.CommentCount - c.rate_4)*100/c.rate_4,1) as rate_4_diff,

        a.Score5Count/a.CommentCount as rate_5,
        c.rate_5 as category_rate_5,
        Format((a.Score5Count/a.CommentCount - c.rate_5)*100/c.rate_5,1) as rate_5_diff,

        a.dt as item_origin_dt,
        c.dt as category_origin_dt,
        c.origin_dt as raw_origin_dt

        FROM

        jd_item_comment_count_latest a
        left JOIN
        jd_item_category b
        on a.SkuId = b.sku_id and b.sku_id is not NULL
        left join
        jd_analytic_category_rating_latest c
        on b.category_id = c.category_id
        left join
        jd_category d
        on d.id = c.category_id
        where a.CommentCount>0

    ''' %timeHelper.getNow()

    # print sql
    afr = dbhelper.executeSqlWrite1(sql,is_dirty=True,isolation_type='serializable')

    return afr


if __name__ == "__main__":

    calculate_rating_diff()

