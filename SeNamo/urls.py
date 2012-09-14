from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to


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
    url(r'^search$','app.views.search'),
    url(r'^category/(?P<category_id>\d+)/$', 'app.views.view_category'),
    url(r'^category/new$', 'app.views.add_category'),
    url(r'^category/(?P<category_id>\d+)/edit$', 'app.views.edit_category'),
    url(r'^category/(?P<category_id>\d+)/delete$', 'app.views.delete_category'),

    url(r'^product/(?P<product_id>\d+)/$', 'app.views.view_product'),
    url(r'^product/new$', 'app.views.add_product'),
    url(r'^product/(?P<product_id>\d+)/edit$', 'app.views.edit_product'),
    url(r'^product/(?P<product_id>\d+)/delete$','app.views.delete_product'),

    url(r'^register$','app.views.register_user'),
    url(r'^login$','app.views.login'),
    url(r'^logout$','django.contrib.auth.views.logout_then_login'),
    url(r'^profile/edit', 'app.views.edit_profile'),

    url(r'^cart$', 'app.views.view_cart'),
    url(r'^testcart$','app.views.add_session'),
    url(r'^clear_cart$','app.views.clear_cart'),
    url(r'^product/(?P<product_id>\d+)/add_to_cart$', 'app.views.add_cart'),
    url(r'^history$','app.views.view_order_history'),

    url(r'^order/(?P<order_id>\d+)/$', 'app.views.view_order_detail'),

    url(r'^checkout/$',redirect_to, {'url': '/checkout/payment'}),
    url(r'^checkout/payment$', 'app.views.checkout_payment'),
    url(r'^checkout/shipping$', 'app.views.checkout_shipping'),
    url(r'^checkout/finish$', 'app.views.checkout_finish'),
    url(r'^checkout/problem$', 'app.views.checkout_problem'),


    url(r'^supplier$', 'app.views.view_supplier'),
    url(r'^supplier/new$', 'app.views.add_supplier'),
    url(r'^supplier/(?P<supplier_id>\d+)/edit$', 'app.views.edit_supplier'),
    url(r'^supplier/(?P<supplier_id>\d+)/delete$', 'app.views.delete_supplier'),

    #url for backOffice
    url(r'^backoffice/login$','app.backOffice.login'),
    url(r'^backoffice/managestock$','app.backOffice.managestock'),
    url(r'^backoffice/managestock/(?P<prod_id>\d+)$','app.backOffice.increaseStock'),
    url(r'^backoffice/packing$','app.backOffice.packing'),
    url(r'^backoffice/packing/(?P<order_id>\d+)$','app.backOffice.proceedPacking'),
    url(r'^backoffice/managecatalog$','app.backOffice.managecatalog'),
    url(r'^backoffice/managecatalog/(?P<category_id>\d+)$','app.backOffice.managecatalog'),


)

#Media
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
)