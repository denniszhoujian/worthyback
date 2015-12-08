# encoding: utf-8

from datasys import dbhelper,crawler_helper

PROPERTY_SPLITTER_LIST = [
    u';',
    u'；',
    u',',
    u'，',
    u'。',
]

def multi_replace(str,splitter_list,replace_into_str = ' '):
    if splitter_list is None or len(splitter_list)==0:
        return [str]
    c = replace_into_str
    for item in splitter_list:
        str = str.replace(item,c)
    return str

def genPropertyTable():

    print("reading...")
    sql = 'select * from jd_item_property_latest'
    retrows = dbhelper.executeSqlRead(sql, is_dirty=True)

    pdict = {}

    for row in retrows:

        p_key = row['p_key']
        if p_key is None:
            continue
        if p_key == '__DEFAULT__' or p_key == u'__DEFAULT__':
            continue
        if len(p_key) > 60:
            # print p_key
            continue

        p_value = row['p_value']
        if (p_value is None):
            continue
        if p_value == u'无':
            # print p_value
            continue
        p_value_nf = multi_replace(p_value,PROPERTY_SPLITTER_LIST,' ')
        lendiff = len(p_value) - len(p_value_nf)
        if lendiff > 5:
            # print p_value
            continue

        sku_id = row['sku_id']
        if sku_id in pdict:
            pold = pdict[sku_id]
            pdict[sku_id] = "%s %s" %(pold,p_value_nf)
        else:
            pdict[sku_id] = p_value_nf

    vlist = []
    for key in pdict:
        vlist.append([key,pdict[key]])

    print("writing to db...")
    return crawler_helper.persist_db_history_and_latest(
        table_name='jd_index_property',
        num_cols=len(vlist[0]),
        value_list=vlist,
        is_many=True,
        need_history=False,
        need_flow=False,
    )


if __name__ == "__main__":
    print genPropertyTable()
