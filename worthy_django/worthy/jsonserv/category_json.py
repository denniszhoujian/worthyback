# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import jsonHelper
from worthy_service import category_service

####################################################################################################
###################    HTTP RESPONSE HERE      #####################################################
####################################################################################################

def getCategoryListAll(request):

    ret = category_service.getServiceCategoryListAll()
    resp = jsonHelper.getJSONPStr(request,ret)
    return HttpResponse(resp, content_type="application/json")
