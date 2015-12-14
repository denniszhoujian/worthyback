# encoding: utf-8

from datasys import dbhelper,crawler_helper
import time

PROPERTY_KEY_BLACK_WORD_LIST = [
    '保质期',
    '其他',
    '其他特征',
]

PROPERTY_VALUE_BLACK_WORD_LIST = [
    '保质期',
    '其他',
    '其他特征',
]

def generate_category_property_mapping():

    # sql = 'select * from jd_category'
    # retrows = dbhelper.executeSqlRead(sql)
    #
    # for row in retrows:
    #     category_id = row['id']
    #     category_name = row['name']
    black_list_clause = '","'.join(PROPERTY_KEY_BLACK_WORD_LIST)
    black_list_clause = '"%s"' %black_list_clause
    sql2 = '''
        select
            sku_id,
            p_key,
            p_value,
            category_id
        from
        jd_item_property_latest a
        left join
        jd_item_category b
        using (sku_id)
		where LENGTH(p_value)>3
		and LENGTH(p_value)<=30
		and p_key<>'__DEFAULT__'
		and LENGTH(p_key)>=6
		and LENGTH(p_key)<=21
		and p_key NOT IN (%s)
    ''' %(black_list_clause)

    vlist = dbhelper.executeSqlRead2(sql2, is_dirty=True)

    sql_cb = '''
        CREATE TABLE jd_analytic_property_latest (
          sku_id bigint(20) DEFAULT NULL,
          p_key varchar(255) DEFAULT NULL,
          p_value varchar(255) DEFAULT NULL,
          category_id varchar(255) DEFAULT NULL,
          KEY skuid_categoryid (sku_id,category_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    '''

    print "now writing to db..."
    t1 = time.time()

    ret = crawler_helper.persist_db_history_and_lastest_empty_first(
        table_name='jd_analytic_property',
        num_cols=len(vlist[0]),
        value_list=vlist,
        is_many=True,
        need_history=False,
        sql_create_table=sql_cb,
    )
    t2 = time.time()
    print "using : %0.0f" %(t2-t1)

    return ret

if __name__ == '__main__':
    generate_category_property_mapping()


