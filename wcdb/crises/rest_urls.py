from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^crises$', 'views.rest.crises'),
    url(r'^crises/(\d+)$', 'views.rest.crisis'),
    url(r'^crises/(\d+)/organizations$', 'views.rest.crisis_orgs'),
    url(r'^crises/(\d+)/people$', 'views.rest.crisis_people'),

    url(r'^people$', 'views.rest.people'),
    url(r'^people/(\d+)$', 'views.rest.person'),
    url(r'^people/(\d+)/organizations$', 'views.rest.person_orgs'),
    url(r'^people/(\d+)/crisis$', 'views.rest.person_crises'),

    url(r'^organizations$', 'views.rest.organizations'),
    url(r'^organizations/(\d+)$', 'views.rest.organization'),
    url(r'^organizations/(\d+)/crisis$', 'views.rest.organization_crises'),
    url(r'^organizations/(\d+)/people$', 'views.rest.organization_people'),
),

