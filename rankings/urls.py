from django.conf.urls import url
from . import views

app_name = 'rankings'

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.IndexViewStudent.as_view(), name='index_student'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    url(r'^(?P<pk>[0-9]+)/$', views.DetailsView.as_view(), name='details'),
    url(r'^university/(?P<pk>[0-9]+)/$', views.UniversityDetailsView.as_view(), name='university_details'),
    url(r'^program/(?P<pk>[0-9]+)/$', views.ProgramDetailsView.as_view(), name='program_details'),

    url(r'^rank/is/$', views.ISListsView.as_view(), name='is_details'),
    url(r'^rank/ba/$', views.BAListsView.as_view(), name='ba_details'),
    url(r'^rank/mba/$', views.MBAListsView.as_view(), name='mba_details'),

    # /rankings/city/add - no reason to add pk as  this is a new city
    url(r'city/add/$', views.CityCreate.as_view(), name='city_add'),
    # /rankings/city/2
    url(r'^city/(?P<pk>[0-9]+)/$', views.CityUpdate.as_view(), name='city_update'),
    # /rankings/city/2/delete/
    url(r'^city/(?P<pk>[0-9]+)/delete/$', views.CityDelete.as_view(), name='city_delete'),

    # /rankings/university/add - no reason to add pk as  this is a new city
    # url(r'^(?P<cityid>[0-9]+)/create_university/$', views.create_university, name='create_university'),
    # # url(r'university/add/$', views.UniversityCreate.as_view(), name='university_add'),
    # # /rankings/university/2
    url(r'^university/(?P<pk>[0-9]+)/update/$', views.UniversityUpdate.as_view(), name='university_update'),
    # # /rankings/university/2/delete/
    url(r'^university/(?P<pk>[0-9]+)/delete/$', views.UniversityDelete.as_view(), name='university_delete'),

    # program
    url(r'^program/(?P<pk>[0-9]+)/update/$', views.ProgramUpdate.as_view(), name='program_update'),
    # # /rankings/program/2/delete/
    url(r'^program/(?P<pk>[0-9]+)/delete/$', views.ProgramDelete.as_view(), name='program_delete'),

    # course
    url(r'^course/(?P<pk>[0-9]+)/update/$', views.CourseUpdate.as_view(), name='course_update'),
    # # /rankings/course/2/delete/
    url(r'^course/(?P<pk>[0-9]+)/delete/$', views.CourseDelete.as_view(), name='course_delete'),

    url(r'^student/$', views.IndexViewStudent.as_view(), name='student_details'),
    url(r'^matches/$', views.MatchesView.as_view(), name='matches_details'),

    url(r'^about1/', views.AboutPageView.as_view(), name='about1'),
]
