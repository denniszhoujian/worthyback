# encoding: utf-8

import json
import timeHelper

for i in xrange(1):
    print i

alist = set([1,3,5,7,9])
blist = set([3,7])

print list(alist-blist)

print timeHelper.getTimeStringFromTimeStamp(1446307200,'%Y-%m-%d %H:%M:%S')