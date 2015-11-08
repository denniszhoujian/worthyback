# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import jsonHelper
from worthy_service import category_service
from datasys import data_config

####################################################################################################
###################    HTTP RESPONSE HERE      #####################################################
####################################################################################################

def getServerDomain(request):

    ret = data_config.SERVER_DOMAIN
    resp = jsonHelper.getJSONPStr(request,ret)
    return HttpResponse(resp, content_type="application/json")
