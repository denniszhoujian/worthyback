from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'worthy_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^commons/server_domain/$', 'worthy.jsonserv.commons.getServerDomain', name='get server domain'),

    url(r'^category/all/$', 'worthy.jsonserv.category_json.getCategoryListAll', name='category all'),

    url(r'^list$', 'worthy.jsonserv.item_list.getDiscountItemsAll', name='getDiscountItemsAll'),

]
