# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import jsonHelper
from worthy_service import sku_service,user_logging_service
import sys
import client_uuid

reload(sys)
sys.setdefaultencoding("utf-8")

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


    querykw = None
    try:
        querykw = request.GET['query']
        # print "query = %s" %querykw
    except:
        pass

    device_id = "_DEFAULT_ID_"
    try:
        device_id = request.GET['device_id']
    except:
        pass

    ip = '0.0.0.0'
    try:
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
    except:
        pass

    need_set_cookie = False
    if device_id == "_DEFAULT_ID_":
        device_id = client_uuid.getClientUUID(request)
        need_set_cookie = True

    ret = None

    use_query = False
    if querykw is not None:
        if len(querykw.strip())>1:
            use_query = True
            query2 = querykw.replace('"','').replace("'",'').replace('OR',' ')
            ret = sku_service.getSkuListByQuery(query2,startpos)

            # record event
            user_logging_service.log_user_event_with_thread(device_id,querykw,'',ip)

    if not use_query:
        ret = sku_service.getSkuListByCatalogID(category_id,startpos)
        user_logging_service.log_user_event_with_thread(device_id,query='',catalog_id=category_id,remote_ip = ip)

    resp = jsonHelper.getJSONPStr(request,ret)
    response = HttpResponse(resp, content_type="application/json")
    if  need_set_cookie:
        response.set_cookie(client_uuid.UUID_COOKIE_NAME,device_id)
    return response
