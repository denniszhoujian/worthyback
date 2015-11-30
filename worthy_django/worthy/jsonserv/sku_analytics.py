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

def getSkuAnalyticsInfo(request):

    sku_id = -9999
    ret = {}
    try:
        sku_id = int(request.GET['sku_id'])
        ret = sku_service.getSingleSku_Mixed_Info(sku_id)
    except:
        print("Invalid request: sku_id error, sku_id requested is (-9999 means none) : %s" %sku_id)

    resp = jsonHelper.getJSONPStr(request,ret)
    return HttpResponse(resp, content_type="application/json")
