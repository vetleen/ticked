from django.conf.urls import patterns, include, url
import os.path

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

static = os.path.join(os.path.dirname(__file__), 'static')

urlpatterns = patterns('',
    
    url(r'^$', 'todotracker.views.frontpageview', name='frontpageview'),
    url(r'^frontpage/$', 'todotracker.views.frontpageview', name='frontpage-by-specific-url'),

    #### TODO MANAGEMENT ####
    url(r'^todos/view/$', 'todotracker.views.viewtodosview', name='viewtodosview'),
    url(r'^todos/view/(\d*)/$', 'todotracker.views.viewtodosview', name='viewspecifictodo'),
    url(r'^todos/add/$', 'todotracker.views.addtodoview', name='addtodoview'),
    url(r'^todos/tick/(\d*)/$', 'todotracker.views.ticktodoview', name='ticktodoview'),
    url(r'^todos/untick/(\d*)/$', 'todotracker.views.unticktodoview', name='unticktodoview'),
    url(r'^todos/view/ticked/$', 'todotracker.views.viewtickedtodoview', name='viewtickedtodo'),
    url(r'^todos/delete/(\d*)/$', 'todotracker.views.deletetodoview', name='deletetodoview'),
    url(r'^todos/edit/(\d*)/$', 'todotracker.views.edittodoview', name='edittodoview'),

    #### USER MANAGEMENT ####    
    url(r'^user/login/$', 'todotracker.views.loginview', name='loginview'),
    url(r'^user/logout/$', 'todotracker.views.logoutview', name='logoutview'),
    url(r'^user/create/$', 'todotracker.views.createnewuserview', name='createnewuserview'),
    url(r'^user/edit/$', 'todotracker.views.edituserview', name='edituserview'),
    url(r'^user/delete/$', 'todotracker.views.deleteuserview', name='deleteuserview'),

	#### STYLESHEETS ####
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': static }),
    # url(r'^ticked/', include('ticked.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
