# encoding: utf-8

def transform_retrows_to_dict(retrows, key_col_name):
    ret = {}
    for row in retrows:
        id = "%s" %row[key_col_name]
        # if id in ret:
        #     print 'id already in dict: id = %s' %id
        ret[id] = row
    return ret

def transform_retrows_to_hashed_arrays(retrows, key_col_name):
    ret = {}
    for row in retrows:
        id = "%s" %row[key_col_name]
        if id in ret:
            ret[id].append(row)
        else:
            ret[id] = [row]
    return ret

def transform_retrows_arrayofdicts_to_arrayoftuples(retrows):
    vlist = []
    for row in retrows:
        tp = []
        for key in row:
            tp.append(row[key])
        vlist.append(tp)
    return vlist

def generate_list_for_db_write(retrows, col_names):
    tlist = []
    for row in retrows:
        tp = []
        for col in col_names:
            val = row[col] if col in row else None
            tp.append(val)
        tlist.append(tp)
    return tlist