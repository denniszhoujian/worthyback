# encoding: utf-8

def transform_retrows_to_dict(retrows, key_col_name):
    ret = {}
    for row in retrows:
        id = "%s" %row[key_col_name]
        if id in ret:
            print 'id already in dict: id = %s' %id
        ret[id] = row
    return ret

def generate_list_for_db_write(retrows, col_names):
    tlist = []
    for row in retrows:
        tp = []
        for col in col_names:
            val = row[col] if col in row else None
            tp.append(val)
        tlist.append(tp)
    return tlist