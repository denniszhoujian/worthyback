# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import jsonHelper
from worthy_service import category_service,catalog_service

####################################################################################################
###################    HTTP RESPONSE HERE      #####################################################
####################################################################################################

def getCategoryListAll(request):

    level = 1
    try:
        level = int(request.GET['level'])
    except:
        print("request param: level: incorrect")
        pass

    # ret = category_service.getServiceCategoryListAll(level)
    ret = catalog_service.getCatalogs()
    resp = jsonHelper.getJSONPStr(request,ret)
    return HttpResponse(resp, content_type="application/json")
