# encoding: utf-8

from worthy_service.sphinxapi import *
from datasys import data_config
import service_config

INDEX_NAME = 'worthy_index_main'

def getSearchResult(query):
    #### SPHINX CLIENT SETUP #####
    cl = SphinxClient()
    cl._host = data_config.SPHINX_HOST
    cl.SetIndexWeights(service_config.SKU_INDEX_WEIGHT_DICT)
    cl.SetSortMode(SPH_SORT_EXPR,clause='@weight*rank_score')
    ##############################

    cl.SetLimits(0,service_config.SKU_LIST_MAX_RECALL_NUM, 0)
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

