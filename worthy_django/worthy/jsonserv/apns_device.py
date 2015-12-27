# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import jsonHelper
from worthy_service import apns_service

####################################################################################################
###################    HTTP RESPONSE HERE      #####################################################
####################################################################################################

def record_device(request):

    ret = {
        'status': -1,
        'msg': 'bad request',
    }

    try:
        original_device_id = request.GET['device_id']
        device_id = original_device_id.strip()
        device_id = device_id[1:len(device_id)-1].replace(' ','')
        platform = request.GET['platform']
        fnret = apns_service.record_device_id(deviceid=device_id, platform=platform, original_deviceid=original_device_id)
        ret['status'] = 0
        ret['msg'] = 'ok'
    except:
        pass

    resp = jsonHelper.getJSONPStr(request,ret)
    return HttpResponse(resp, content_type="application/json")


