# encoding: utf-8

import sys
import json
from datasys import timeHelper
import url_utils
import dbhelper

reload(sys)
sys.setdefaultencoding('utf8')

JD_CATEGORY_WEBSERVICE_URL = "http://dc.3.cn/category/get?callback=getCategoryCallback"
JD_ENC = "GBK"

def loadCategoryList():
    html = url_utils.getWebResponse(JD_CATEGORY_WEBSERVICE_URL,JD_ENC)
    json_str = url_utils.removeJsonP(html)
    obj = json.loads(json_str)
    clist = __extractCategoryList_fromJson__(obj)

    cat_list = []

    for item in clist:
        print item
        vals = item.split('|')
        if len(vals)<4:
            print 'error in length of category line'
            print item
            continue
        cat_name = vals[1]
        vals0 = vals[0]
        cat_id = cat_url = cat_memo = ""
        if '.com' in vals0:
            cat_url = vals0
        else:
            cat_id = vals0
        if len(vals[2]) > 0:
            cat_memo = vals[2]

        if len(cat_id) > 0:
            tp = (cat_id,cat_name, timeHelper.getNow())
            cat_list.append(tp)

    # persist categories
    sql = 'replace into jd_category values(%s,%s,%s)'
    affected_rows = dbhelper.executeSqlWriteMany(sql,cat_list)

    print 'rows affected : jd_category : %s' %affected_rows

    return 0



def __extractCategoryList_fromJson__(json_obj):
    ret_list = []
    clist = json_obj['data']
    for top_level_category_map in clist:
        if 's' in top_level_category_map:
            ret_list += __extractCascadedSN__(top_level_category_map['s'])
    return ret_list

def __extractCascadedSN__(root_s_list):
    if len(root_s_list) == 0:
        return []
    nslist = []
    for nsmap in root_s_list:
        nslist.append(nsmap['n'])
        nslist += __extractCascadedSN__(nsmap['s'])
    return nslist



if __name__ == "__main__":

    loadCategoryList()