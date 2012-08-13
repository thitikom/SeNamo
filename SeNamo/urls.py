from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SeNamo.views.home', name='home'),
    # url(r'^SeNamo/', include('SeNamo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^category/(?P<category_id>\d+)/$', 'app.views.view_category'),
    url(r'^product/(?P<product_id>\d+)/$', 'app.views.view_product'),
    url(r'^product/new$', 'app.views.add_product'),
    url(r'^product/(?P<product_id>\d+)/edit$', 'app.views.edit_product'),
    url(r'^category/new$', 'app.views.add_category'),
    url(r'^category/(?P<category_id>\d+)/edit$', 'app.views.edit_category'),

)
