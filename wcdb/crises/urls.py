from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    #url(r'^$', 'crises.views.index'),
    url(r'^crises/$','crises.views.crises_list'),
    url(r'^crises/(\d+)/$', 'crises.views.crisis_index'),
    url(r'^organizations/(\d+)/$', 'crises.views.org_index'),
    url(r'^people/(\d+)/$', 'crises.views.person_index'),
)