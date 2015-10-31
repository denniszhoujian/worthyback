# encoding: utf-8

import json
import timeHelper
import urllib2
import mylog


# for i in xrange(1):
#     print i
#
# alist = set([1,3,5,7,9])
# blist = set([3,7])
#
# print list(alist-blist)
#
# print timeHelper.getTimeStringFromTimeStamp(1446307200,'%Y-%m-%d %H:%M:%S')
#
# resp = urllib2.urlopen('http://item.jd.com/1310729.html')
# html = resp.read()
# html2 = html.decode('gb18030')
# print html2
#


adict = {
            "SkuId": 1279827,
            "ProductId": 1279827,
            "Score1Count": 261,
            "Score2Count": 80,
            "Score3Count": 299,
            "Score4Count": 1211,
            "Score5Count": 21239,
            "ShowCount": 1541,
            "CommentCount": 23090,
            "AverageScore": 5,
            "GoodCount": 22450,
            "GoodRate": 0.973,
            "GoodRateShow": 97,
            "GoodRateStyle": 146,
            "GeneralCount": 379,
            "GeneralRate": 0.016,
            "GeneralRateShow": 2,
            "GeneralRateStyle": 2,
            "PoorCount": 261,
            "PoorRate": 0.011,
            "PoorRateShow": 1,
            "PoorRateStyle": 2
        }

print list(adict)