from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    #url(r'^$', 'crises.views.index'),
    url(r'^(crises|organizations|people)/$','crises.views.links'),
    
    url(r'^crises/(\d+)/$', 'crises.views.crisis_index'),

    url(r'^organizations/(\d+)/$', 'crises.views.org_index'),

    url(r'^people/(\d+)/$', 'crises.views.person_index'),

    url(r'^wordcloud/$','crises.views.wordcloud_list'),

    url(r'^wordcloud/(\w+)$','crises.views.wordclouds'),
    
    url(r'^sqlqueries/$','crises.views.sqlqueries_list'),

    url(r'^sqlqueries/(\d+)$','crises.views.sqlquery'),

    url(r'^api/', include('crises.rest_urls')),

    #############################################################
    url(r'^search/', 'crises.views.search'),

    url(r'^tests/', 'crises.views.tests'),
    #############################################################

    url(r'^tests', 'crises.views.tests'),
)
