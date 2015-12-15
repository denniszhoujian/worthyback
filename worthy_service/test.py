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


test_expedia()