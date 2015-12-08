# encoding: utf-8

from sphinxapi import *
from datasys import data_config


INDEX_NAME = 'worthy_index_main'

#### SPHINX CLIENT SETUP #####
cl = SphinxClient()
cl._host = data_config.SPHINX_HOST
cl.SetSortMode(SPH_SORT_EXTENDED,clause='rank_score DESC')

##############################

def getCatalogResults():

    cl.SetLimits(0,30,0)
    ret = cl.Query('阿玛尼')
    return ret

if __name__ == "__main__":

    ret = getCatalogResults()
    print ret
    print len(ret['matches'])
