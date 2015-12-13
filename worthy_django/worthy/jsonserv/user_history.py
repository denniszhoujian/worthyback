# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import jsonHelper
from worthy_service import user_history_service

####################################################################################################
###################    HTTP RESPONSE HERE      #####################################################
####################################################################################################

def getUserListHistory(request):

    ret = {
        'query':[],
        'catalog':[],
    }
    try:
        device_id = request.GET['device_id']
        if device_id is not None:
            ret['query'] = user_history_service.getQueryHistory(device_id)
            ret['catalog'] = user_history_service.getCatalogHistory(device_id)
    except:
        pass

    resp = jsonHelper.getJSONPStr(request,ret)
    return HttpResponse(resp, content_type="application/json")

