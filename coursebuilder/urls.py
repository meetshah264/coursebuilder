# urls.py

from django.urls import path
from . import views
from .views import * 

urlpatterns = [

  path('', views.home, name='home'),

  # Authentication
  path('login/', views.login_here, name='login_here'),
  path('signup/', views.signup, name='signup'),
  path('logout/', views.logout_here, name='logout_here'),
  path('forgotpassword/', views.forgot_password, name='forgot_password'),

  # Course-related URLs
  path('courses/', views.course_list, name='course_list'),
  path('course/<int:course_id>/', views.course_detail, name='course_detail'),
  path('course/create/', views.course_create, name='course_create'),
  path('course/<int:course_id>/update/', views.course_update, name='course_update'),
  path('course/<int:course_id>/delete/', views.course_delete, name='course_delete'),

  # Assignment-related URLs
  path('course/<int:course_id>/assignments/', views.assignment_list, name='assignment_list'),
  path('course/<int:course_id>/assignment/create/', views.assignment_create, name='assignment_create'),
  path('course/<int:course_id>/assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
  path('course/<int:course_id>/assignment/<int:assignment_id>/update/', views.assignment_update, name='assignment_update'),
  path('course/<int:course_id>/assignment/<int:assignment_id>/delete/', views.assignment_delete, name='assignment_delete'),
  path('course/<int:course_id>/assignment/<int:assignment_id>/download/', views.assignment_download, name='assignment_download'),

  #grade
  path('grades/', views.grade_student, name='grade_student'),
  path('gradesprof/', views.grade_professor, name='grade_professor'),

  #aboutus
  path('aboutus/', AboutUsView.as_view(), name='aboutus'),

  #Membership-related URLs
  path('course/<int:course_id>/membership/', views.membership_detail, name='membership_details'),

  # Events-related URLs
  path('events/', views.event_list, name='event_list'),
  path('event/<int:event_id>/', views.event_detail, name='event_detail'),
  path('event/create/', views.event_create, name='event_create'),
  path('event/<int:event_id>/update/', views.event_update, name='event_update'),
  path('event/<int:event_id>/delete/', views.event_delete, name='event_delete'),
]

