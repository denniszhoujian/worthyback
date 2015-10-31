# encoding: utf-8

import dbhelper

def persist_db_history_and_latest(table_name, num_cols, value_list, is_many=True):
    tbl_latest = '%s_latest' %table_name
    ps_list = []
    for i in xrange(num_cols):
        ps_list.append('%s')
    values_str = ','.join(ps_list)

    sql = 'replace into %s values(%s)' %(table_name,values_str)
    affected_rows = dbhelper.executeSqlWriteMany(sql,value_list)
    sql2 = 'replace into %s values(%s)' %(tbl_latest,values_str)
    affected_rows2 = dbhelper.executeSqlWriteMany(sql2,value_list)
    status = -1
    if affected_rows>0 and affected_rows2>0:
        status = 0
    ret = {
        'status':status,
        'affected_rows':affected_rows,
        'affected_rows2':affected_rows2
    }
    return ret


if __name__ == '__main__':
    persist_db_history_and_latest('ok',5,[])