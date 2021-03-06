# encoding: utf-8

import sku_index_access
import sku_service
import service_config
from collections import defaultdict

def rerank_list_query(query):
    idlist = sku_index_access.getSearchResult(query)
    thumb_list = list(sku_service.getWorthyInfo_of_skuid_list(idlist))
    retlist = _rerank_thumb_list(thumb_list,apply_category_mixer=False)
    return retlist

def rerank_list(idlist, apply_category_mixer=True):
    thumb_list = list(sku_service.getWorthyInfo_of_skuid_list(idlist))
    retlist = _rerank_thumb_list(thumb_list,apply_category_mixer=apply_category_mixer)
    return retlist # was thumb_list

def _rerank_thumb_list(thumb_list, apply_category_mixer = False):
    dict_comment = defaultdict(int)
    dict_catalog = defaultdict(int)

    total = len(thumb_list)
    maxnum = service_config.SKU_LIST_RERANK_TOP_NUM
    if total > maxnum:
        total = maxnum

    for i in xrange(total):
        fulfill = 0
        for k in range(i,total):

            thumb = thumb_list[k]
            comment_count = thumb['comment_count']
            if comment_count is None:
                pass
            catalog_id = thumb['catalog_id']

            comment_r = dict_comment[comment_count]
            catalog_r = dict_catalog[catalog_id]

            if ( (i-comment_r)>30 or comment_r == 0 ) and ( (not apply_category_mixer) or ( (i-catalog_r)>10 or catalog_r == 0) ):
                # record pos
                dict_comment[comment_count] = i
                dict_catalog[catalog_id] = i
                # re-rank list
                if k!=i:
                    row = thumb_list[k]
                    thumb_list.pop(k)
                    thumb_list.insert(i,row)
                    # print 'haha'
                # done
                fulfill = 1
                break
            else:
                pass #for debug only
        if fulfill==0:
            break

    retlist = []
    for thumb in thumb_list:
        retlist.append(thumb['sku_id'])
    #return thumb_list   # it's ok to not return the list, but this is simple and consistent for use
    return retlist

if __name__ == "__main__":
    print rerank_list_query('包')