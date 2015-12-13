# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import jsonHelper
from worthy_service import catalog_service

####################################################################################################
###################    HTTP RESPONSE HERE      #####################################################
####################################################################################################

def getQueryIndicator(request):

    ret = {
        'category': [],
        'property': [],
    }
    try:
        query = request.GET['query']
        ret = catalog_service.get_indicator_given_part_of_query(query)
    except:
        pass
    resp = jsonHelper.getJSONPStr(request,ret)
    return HttpResponse(resp, content_type="application/json")
