# encoding: utf-8

from worthy_service.sphinxapi import *
from datasys import data_config

INDEX_NAME = 'worthy_index_main'
INDEX_MAX_RECALL = 2500


def getSearchResult(query):
    #### SPHINX CLIENT SETUP #####
    cl = SphinxClient()
    cl._host = data_config.SPHINX_HOST
    cl.SetSortMode(SPH_SORT_EXTENDED,clause='rank_score DESC')
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

    ret = getSearchResult('衣')
    print ret
    print len(ret)

