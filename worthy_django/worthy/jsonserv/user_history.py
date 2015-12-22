# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import jsonHelper
from worthy_service import user_history_service
import client_uuid

####################################################################################################
###################    HTTP RESPONSE HERE      #####################################################
####################################################################################################

def getUserListHistory(request):

    ret = {
        'query':[],
        'catalog':[],
    }
    if 'device_id' in request.GET:
        device_id = request.GET['device_id']
    else:
        device_id = client_uuid.getClientUUID(request)

    if device_id is not None:
        ret['query'] = user_history_service.getQueryHistory(device_id)
        ret['catalog'] = user_history_service.getCatalogHistory(device_id)

    resp = jsonHelper.getJSONPStr(request,ret)
    return HttpResponse(resp, content_type="application/json")

