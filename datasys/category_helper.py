# encoding: utf-8

import dbhelper

def __load_white_categories___():
    sql = 'select category_id from jd_category_white_list limit 100'
    retrows = dbhelper.executeSqlRead(sql)
    retlist = []
    for row in retrows:
        retlist.append(row['category_id'])
    return retlist

def __expand_to_sub_categories__(category_id):
    sql = 'select distinct id from jd_category where id like "%s-%%"' %category_id
    retrows = dbhelper.executeSqlRead(sql)
    retlist = []
    for row in retrows:
        retlist.append(row['id'])
    return retlist

def __is_unique_in_list__(id,id_list):
    for item in id_list:
        if item.find(id)==0 and len(item)!=len(id):
            return 0
    return 1

def __remove_duplicate_categories__(category_list):
    retlist = []
    for cat in category_list:
        if __is_unique_in_list__(cat,category_list)==1:
            retlist.append(cat)
    return retlist

def load_all_white_sub_categories():
    cat_list = __load_white_categories___()
    sub_cat_list = []
    for cat_id in cat_list:
        sub_cat_list = sub_cat_list + __expand_to_sub_categories__(cat_id)
    task_list = __remove_duplicate_categories__(sub_cat_list)
    return task_list