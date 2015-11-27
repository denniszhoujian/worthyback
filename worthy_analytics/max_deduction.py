# encoding: utf-8

from datasys import dbhelper
import logging

def calculate_max_deduction():

    sql1 = 'drop table if exists jd_analytic_promo_deduction_max'

    sql2 = '''
        CREATE TABLE jd_analytic_promo_deduction_max (

          sku_id bigint(20) NOT NULL,
          add_time datetime NOT NULL,
          price float NOT NULL,
          is_repeat tinyint(4) NOT NULL,
          reach float NOT NULL,
          deduction float NOT NULL,
          max_deduction float NOT NULL,
          dr_ratio float NOT NULL,
          maxp_ratio float NOT NULL,
          max_deduction_ratio float NOT NULL,
          content varchar(255) DEFAULT NULL,
          adurl varchar(255) DEFAULT NULL,
          origin_time datetime NOT NULL,
          this_update_time datetime not NULL,
          sku_id_alias bigint(2) NOT NULL,
          reach_2 float NOT NULL,
          deduction_2 float NOT NULL,
          max_dr_ratio float NOT NULL,
          discount_score_2 float NOT NULL,

          KEY skuid (sku_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    '''

    sql3 = '''
        insert into jd_analytic_promo_deduction_max

        select *

        from

        (
            select
                sku_id,
                add_time,
		        price,
                is_repeat,
                reach,
                deduction,
                max_deduction,
                dr_ratio,
                maxp_ratio,
                single_discount_rate,
                content,
                adurl,
                origin_time,
                CURRENT_TIMESTAMP() as this_update_time
                FROM
                ( select * from
                  jd_analytic_promo_deduction_latest order by single_discount_rate DESC
                ) kk
                group by sku_id
        ) pp

        left join

        (
            select
                sku_id as sku_id_alias,
                reach as reach_2,
                deduction as deduction_2,
                max(dr_ratio) as max_dr_ratio,
		        discount_score_2
                FROM
                ( select *,
		  if(reach>price, pow(price/reach,1.0)*dr_ratio,single_discount_rate) as discount_score_2
		  from
                  jd_analytic_promo_deduction_latest
		  order by discount_score_2 DESC
                ) rr
                group by sku_id
        ) qq

        on pp.sku_id = qq.sku_id_alias

    '''

    affected_rows = -1
    conn = dbhelper.getConnection()
    try:
        cursor1 = conn.cursor()
        ar1 = cursor1.execute(sql1)
        ar2 = cursor1.execute(sql2)
        if ar2 != 0:
            raise Exception('Create deduction_max table failed...')
        ar3 = cursor1.execute(sql3)
        conn.commit()
        affected_rows = cursor1.rowcount
    except Exception as e:
        conn.rollback()
        print e
    finally:
        conn.close()
    return affected_rows


if __name__ == "__main__":

    print calculate_max_deduction()