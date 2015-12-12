# encoding: utf-8

from worthy_service.sphinxapi import *
from datasys import data_config

INDEX_NAME = 'worthy_index_main'
INDEX_MAX_RECALL = 2500

INDEX_WEIGHT_DICT = {
    'title': 7,
    'category_name':10,
    'catalog_name':4,
    'name_deduction':10,
    'name_discount':10,
    'name_lowest':10,
    'property_text':4,
    'category_text':4,
}

def getSearchResult(query):
    #### SPHINX CLIENT SETUP #####
    cl = SphinxClient()
    cl._host = data_config.SPHINX_HOST
    cl.SetIndexWeights(INDEX_WEIGHT_DICT)
    cl.SetSortMode(SPH_SORT_EXPR,clause='@weight*rank_score')
    ##############################

    cl.SetLimits(0,INDEX_MAX_RECALL, 0)
    ret = cl.Query(query)

    idlist = []
    try:
        for match in ret['matches']:
            idlist.append(match['id'])
    except:
        pass

    return idlist

if __name__ == "__main__":

    ret = getSearchResult('键盘')
    print ret
    print len(ret)

