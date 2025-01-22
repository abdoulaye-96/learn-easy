"""
url de l'application core
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('administrateur/', views.admin_dashboard, name='admin_dashboard'),
    path('professor/', views.professor_dashboard, name='professor_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
