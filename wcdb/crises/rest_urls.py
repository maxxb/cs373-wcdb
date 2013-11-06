from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^crises$', 'rest_views.crises'),
    url(r'^crises/(\d+)$', 'rest_views.crisis'),
    url(r'^crises/(\d+)/organizations$', 'rest_views.crisis_orgs'),
    url(r'^crises/(\d+)/people$', 'rest_views.crisis_people'),

    url(r'^people$', 'rest_views.people'),
    url(r'^people/(\d+)$', 'rest_views.person'),
    url(r'^people/(\d+)/organizations$', 'rest_views.person_orgs'),
    url(r'^people/(\d+)/crisis$', 'rest_views.person_crises'),

    url(r'^organizations$', 'rest_views.organizations'),
    url(r'^organizations/(\d+)$', 'rest_views.organization'),
    url(r'^organizations/(\d+)/crisis$', 'rest_views.organization_crises'),
    url(r'^organizations/(\d+)/people$', 'rest_views.organization_people'),
),

