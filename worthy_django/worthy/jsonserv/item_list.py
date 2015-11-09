# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import jsonHelper
from worthy_service import sku_service

####################################################################################################
###################    HTTP RESPONSE HERE      #####################################################
####################################################################################################

def getDiscountItemsAll(request):

    startpos = 0
    try:
        startpos = int(request.GET['startpos'])
    except:
        # FRAME is SET TO 0
        pass

    category_id = "_ALL_"
    min_price = min_discount_rate = None
    try:
        category_id = request.GET['category_id']
        print "ok, cateid = %s" %category_id
        min_price = float(request.GET['min_price'])
        min_discount_rate = float(request.GET['max_discount_rate'])
        category_id = request.GET['category_id']
        print "ok, cateid = %s" %category_id
    except:
        pass

    ret = None
    if min_price is not None and min_discount_rate is not None and min_price > 0 and min_discount_rate > 0 and min_discount_rate < 1:
        ret = sku_service.getDiscountItemsAll(category_id, startpos, min_price,min_discount_rate)
    else:
        ret = sku_service.getDiscountItemsAll(category_id,startpos)

    resp = jsonHelper.getJSONPStr(request,ret)
    return HttpResponse(resp, content_type="application/json")
