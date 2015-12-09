# encoding: utf-8

from datasys import dbhelper, crawler_helper

def generate_index():
    catdict = getMergedCategoryInfo()
    vlist = []
    for key in catdict:
        vlist.append([key,catdict[key]])
    sqlcb = '''
        CREATE TABLE jd_index_category_latest (
          category_id varchar(255) NOT NULL,
          category_text varchar(255) NOT NULL,
          PRIMARY KEY (category_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    '''
    return crawler_helper.persist_db_history_and_lastest_empty_first(
        table_name='jd_index_category',
        num_cols=len(vlist[0]),
        value_list=vlist,
        is_many=True,
        need_history=False,
        sql_create_table=sqlcb,
    )

def _get_display_name_dict():

    sql = 'select * from jd_category_show'
    retrows = dbhelper.executeSqlRead(sql)

    catdict = {}
    for row in retrows:
        cat_id = row['category_id_prefix']
        cat_text = "%s %s" %(row['category_prefix_name'],row['display_name'])
        catdict[cat_id] = cat_text
    return catdict

def _get_category_all():
    sql = 'select * from jd_category'
    retrows = dbhelper.executeSqlRead(sql)
    catdict = {}
    for row in retrows:
        cat_id = row['id']
        cat_text = row['name'].replace('/',' ')
        catdict[cat_id] =cat_text
    return catdict


def _expand_to_full_path_given_leaf(cat_dict, leaf_id, leaf_name):
    for id in cat_dict:
        if leaf_id.startswith(id) and leaf_id!=id:
            new_leaf_name = "%s %s" %(cat_dict[id],cat_dict[leaf_id])
            new_leaf_id = id
            return _expand_to_full_path_given_leaf(cat_dict,new_leaf_id,new_leaf_name)
    return leaf_name

def _get_full_path_category_dict():
    cat_dict = _get_category_all()
    for leaf_id in cat_dict:
        leaf_name = cat_dict[leaf_id]
        cat_dict[leaf_id] = _expand_to_full_path_given_leaf(cat_dict, leaf_id, leaf_name)
    return cat_dict

def _merge_dicts(full_dict,display_dict):

    for key in full_dict:
        for key2 in display_dict:
            if key.startswith(key2) and key!=key2:
                full_dict[key] = "%s %s" %(full_dict[key],display_dict[key2])
                break
    return full_dict


def getMergedCategoryInfo():

    full_dict = _get_full_path_category_dict()
    display_dict = _get_display_name_dict()
    return _merge_dicts(full_dict,display_dict)


if __name__ == '__main__':
    # ret = getMergedCategoryInfo()
    # for key in ret:
    #     print key
    #     print ret[key]
    #     print '-'*30
    ret = generate_index()
    print ret
