from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'worthy_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^commons/server_domain/$', 'worthy.jsonserv.commons.getServerDomain', name='get server domain'),

    url(r'^category/list$', 'worthy.jsonserv.category_json.getCategoryListAll', name='category all'),

    url(r'^sku/list$', 'worthy.jsonserv.item_list.getDiscountItemsAll', name='getDiscountItemsAll'),
    url(r'^sku/info$', 'worthy.jsonserv.sku_analytics.getSkuAnalyticsInfo', name='getSkuAnalyticsInfo'),

    url(r'^user/history$', 'worthy.jsonserv.user_history.getUserListHistory', name='getUserListHistory'),

    url(r'^query/indicator$', 'worthy.jsonserv.query_indicator.getQueryIndicator', name='getQueryIndicator'),

]
