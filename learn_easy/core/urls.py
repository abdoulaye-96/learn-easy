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

    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/new/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # module
    path('modules/', views.module_list, name='module_list'),
    path('modules/<int:pk>/', views.module_detail, name='module_detail'),
    path('modules/new/', views.module_create, name='module_create'),
    path('modules/<int:pk>/edit/', views.module_update, name='module_update'),
    path('modules/<int:pk>/delete/', views.module_delete, name='module_delete'),

    # Courses
#     path('courses/', views.course_list, name='course_list'),
#     path('courses/<int:pk>/', views.course_detail, name='course_detail'),
#     path('courses/new/', views.course_create, name='course_create'),
#     path('courses/<int:pk>/edit/', views.course_update, name='course_update'),
#     path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
]
