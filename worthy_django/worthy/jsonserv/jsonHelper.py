# encoding : utf-8

import json
from datetime import date, datetime
from django.core.serializers.json import DjangoJSONEncoder

class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        # if isinstance(obj, datetime.datetime):
        #     return int(mktime(obj.timetuple()))
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def responseBadRequest(reason="unknown"):
    resp = {
        "status": -1,
        "msg": "bad-request",
        "reason": reason
    }
    return HttpResponse(resp, content_type="application/json")

def getJSONPStr(request,rdict):
    #jtext = json.dumps(rdict)
    jtext = None
    callback = None
    try:
        jtext = json.dumps(rdict,cls=DjangoJSONEncoder)
        if 'ShowDemo!' in jtext:
            print 'Password found in json response!!!!&%(*&%*&%(&^*(&^(*&^(&^)^*(&^*'
    except:
        pass
    try:
        callback = request.GET['callback']
    except:
        pass
    if callback is None:
        return jtext
    return callback + '(' + jtext + ');'

def makeRetrows_Dot_Underscore(retrows):
    if retrows is None:
        return None
    rlist = retrows
    r2list = []
    for tdict in rlist:
        t2dict = {}
        for tkey in tdict:
            if '.' in tkey:
                newkey = tkey.replace('.','___')
                t2dict[newkey] = tdict[tkey]
            else:
                t2dict[tkey] = tdict[tkey]
        r2list.append(t2dict)
    return r2list

