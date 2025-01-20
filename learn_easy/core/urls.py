"""
urls de l'application core
"""
from django.urls import path
from .views import home, CourseListAPIView, RegisterAPIView, CourseCreateAPIView
from .views import dashboard



urlpatterns = [
    path('', home, name='home'),  # Page d'accueil
    path('api/courses/', CourseListAPIView.as_view(), name='course-list'),  # Endpoint API
    path('api/register/', RegisterAPIView.as_view(), name='register'),  # Endpoint API registration
    path('api/courses/create/', CourseCreateAPIView.as_view(), name='create-course'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]
