from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

# Setting
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SeNamo.views.home', name='home'),
    # url(r'^SeNamo/', include('SeNamo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'app.views.index'),
    url(r'^category/(?P<category_id>\d+)/$', 'app.views.view_category'),
    url(r'^category/new$', 'app.views.add_category'),
    url(r'^category/(?P<category_id>\d+)/edit$', 'app.views.edit_category'),
    url(r'^category/(?P<category_id>\d+)/delete$', 'app.views.delete_category'),

    url(r'^product/(?P<product_id>\d+)/$', 'app.views.view_product'),
    url(r'^product/new$', 'app.views.add_product'),
    url(r'^product/(?P<product_id>\d+)/edit$', 'app.views.edit_product'),
    url(r'^product/(?P<product_id>\d+)/delete$','app.views.delete_product'),

    url(r'^register$','app.views.register_user'),
    #url(r'^login$','django.contrib.auth.views.login',{'template_name': 'login_user.html'}),
    url(r'^login$','app.views.login'),
    url(r'^logout$','app.views.logout'),
    #url(r'^logout$','django.contrib.auth.views.logout',{'template_name': 'logout_user.html'}),
)

#Media
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
)