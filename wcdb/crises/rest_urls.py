from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^crises$', 'crises.rest_views.crises'),
    url(r'^crises/(\d+)$', 'crises.rest_views.crisis'),
    url(r'^crises/(\d+)/organizations$', 'crises.rest_views.crisis_orgs'),
    url(r'^crises/(\d+)/people$', 'crises.rest_views.crisis_people'),

    url(r'^people$', 'crises.rest_views.people'),
    url(r'^people/(\d+)$', 'crises.rest_views.person'),
    url(r'^people/(\d+)/organizations$', 'crises.rest_views.person_orgs'),
    url(r'^people/(\d+)/crises$', 'crises.rest_views.person_crises'),

    url(r'^organizations$', 'crises.rest_views.organizations'),
    url(r'^organizations/(\d+)$', 'crises.rest_views.organization'),
    url(r'^organizations/(\d+)/crises$', 'crises.rest_views.organization_crises'),
    url(r'^organizations/(\d+)/people$', 'crises.rest_views.organization_people'),
)

