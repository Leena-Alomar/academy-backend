from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.Home.as_view(), name='home'),
    # path('course/<int:coures_id>/', views.CourseDetailsView.as_view(), name='course-detail'),
    # path('schedule/<int:schedule_id>/', views.ScheduleDetailsView.as_view(), name='schedule-detail'),
    # path('schedule/<int:schedule_id>/lesson/<int:lesson_id>/', views.ScheduleLessonRelationView.as_view(), name='schedule-lesson-relation'),
    # path('lesson/<int:lesson_id>/', views.LessonDetailsView.as_view(), name='lesson-detail'),
    # path('schedule/<int:schedule_id>/lesson/<int:lesson_id>/', views.LessonRelationView.as_view(), name='lesson-relation'),
    path('users/signup/', views.CreateUserView.as_view(), name='signup'),
    path('users/login/', views.LoginView.as_view(), name='login'),
    path('users/token/refresh/', views.VerifyUserView.as_view(), name='token_refresh'),
]