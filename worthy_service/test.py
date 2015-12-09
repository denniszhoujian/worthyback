__author__ = 'Dennis'

# uwsgi --http :8080 --chdir /Users/Dennis/webcode/worthyback/worthy_django --module django_wsgi --buffer-size=32768
# uwsgi --http :8080 --chdir /Users/Dennis/PycharmProjects/myproj/jsonport --module django_wsgi --buffer-size=32768

alist = [1,2,3,4,5]
k = alist[3]
alist.pop(3)
alist.insert(2,k)
print alist