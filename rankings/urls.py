from django.conf.urls import url
from . import views

app_name = 'rankings'

urlpatterns = [
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.IndexView2.as_view(), name='index2'),

    url(r'^(?P<pk>[0-9]+)/$', views.DetailsView.as_view(), name='details'),

    # /rankings/city/add - no reason to add pk as  this is a new city
    url(r'city/add/$', views.CityCreate.as_view(), name='city_add'),
    # /rankings/city/2
    url(r'^city/(?P<pk>[0-9]+)/$', views.CityUpdate.as_view(), name='city_update'),
    # /rankings/city/2/delete/
    url(r'^city/(?P<pk>[0-9]+)/delete/$', views.CityDelete.as_view(), name='city_delete'),

    # /rankings/university/add - no reason to add pk as  this is a new city
    url(r'university/add/$', views.UniversityCreate.as_view(), name='university_add'),
    # /rankings/university/2
    url(r'^university/(?P<pk>[0-9]+)/$', views.UniversityUpdate.as_view(), name='university_update'),
    # /rankings/university/2/delete/
    url(r'^university/(?P<pk>[0-9]+)/delete/$', views.UniversityDelete.as_view(), name='university_delete'),
]
