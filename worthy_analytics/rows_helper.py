# encoding: utf-8

def transform_retrows_to_dict(retrows, key_col_name):
    ret = {}
    for row in retrows:
        id = "%s" %row[key_col_name]
        ret[id] = row
    return ret