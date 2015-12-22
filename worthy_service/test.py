#encoding: utf-8
__author__ = 'Dennis'

# uwsgi --http :8080 --chdir /Users/Dennis/webcode/worthyback/worthy_django --module django_wsgi --buffer-size=32768
# uwsgi --http :8080 --chdir /Users/Dennis/PycharmProjects/myproj/jsonport --module django_wsgi --buffer-size=32768

alist = [1,2,3,4,5]
k = alist[3]
alist.pop(3)
alist.insert(2,k)
print alist

import urllib2
from datasys import url_utils

def test_expedia():
    html = url_utils._getWebResponse('http://www.expedia.com')
    print html


# test_expedia()

print u'其他' in [u'其他',u'我们',]

import uuid
print uuid.uuid1()
print uuid.uuid1()