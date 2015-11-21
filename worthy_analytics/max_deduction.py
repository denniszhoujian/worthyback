# encoding: utf-8

from datasys import dbhelper

def calculate_max_deduction():

    sql1 = 'drop table if exists jd_analytic_promo_deduction_max'

    sql2 = '''
        CREATE TABLE jd_analytic_promo_deduction_max (
  sku_id_alias bigint(20) NOT NULL,
  max_deduction_ratio float NOT NULL,
  sku_id bigint(20) NOT NULL,
  add_time datetime NOT NULL,
  title varchar(255) NOT NULL,
  price decimal(10,0) NOT NULL,
  is_repeat tinyint(4) NOT NULL,
  reach float NOT NULL,
  deduction float NOT NULL,
  max_deduction float NOT NULL,
  dr_ratio float NOT NULL,
  maxp_ratio float NOT NULL,
  single_discount_rate float NOT NULL,
  category_id varchar(255) NOT NULL,
  category_name varchar(255) DEFAULT NULL,
  pid varchar(255) NOT NULL,
  code varchar(255) NOT NULL,
  name varchar(255) NOT NULL,
  content varchar(255) NOT NULL,
  adurl varchar(255) DEFAULT NULL,
  origin_time datetime NOT NULL,
  KEY skuid (sku_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
    '''

    sql3 = '''
        insert into jd_analytic_promo_deduction_max

        select * from
        (
        select
        sku_id as sku_id_alias,
        max(single_discount_rate) as max_deduction_ratio
        FROM
        jd_analytic_promo_deduction_latest
        group by sku_id
        ) aa

        left join

        jd_analytic_promo_deduction_latest bb

        on
        aa.sku_id_alias = bb.sku_id
        and ABS(aa.max_deduction_ratio-bb.single_discount_rate)<0.01
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