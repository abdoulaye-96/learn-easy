"""
url de l'application core
"""
from django.urls import path
from . import views
from django.conf.urls.static import static, settings

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
    path('courses/create/', views.create_course, name='course_create'),  # Assurez-vous que cette ligne existe
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/update/<int:course_id>/', views.course_update, name='course_update'),
    path('courses/delete/<int:course_id>/', views.course_delete, name='course_delete'),
    path('courses/<int:course_id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),

    # Modules
    path('courses/<int:course_id>/modules/', views.module_list, name='module_list'),
    path('modules/<int:module_id>/', views.module_detail, name='module_detail'),
    path('create-module/', views.create_module, name='create_module'),
    path('modules/<int:module_id>/update/', views.module_update, name='module_update'),
    path('modules/<int:module_id>/delete/', views.module_delete, name='module_delete'),
    path('courses/<int:course_id>/modules/', views.module_list, name='module_list'),
    path('courses/<int:course_id>/modules/create/', views.create_module, name='create_module'),

    # Lessons
    path('modules/<int:module_id>/lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('create-lesson/<int:module_id>/', views.create_lesson, name='create_lesson'),
    path('lessons/<int:module_id>/update/', views.lesson_update, name='lesson_update'),
    path('lessons/<int:module_id>/delete/', views.lesson_delete, name='lesson_delete'),
    path('modules/<int:module_id>/', views.module_detail, name='module_detail'),
    path('lessons/<int:lesson_id>/update/', views.lesson_update, name='lesson_update'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('create-lesson/<int:module_id>/', views.create_lesson, name='create_lesson'),




    # Assignments
    path('modules/<int:module_id>/assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('create-assignment/<int:module_id>/<int:course_id>/', views.create_assignment, name='create_assignment'),
    path('assignment/<int:assignment_id>/update/', views.assignment_update, name='assignment_update'),
    path('assignment/<int:assignment_id>/delete/', views.assignment_delete, name='assignment_delete'),
    # path('module/<int:module_id>/assignment_id/', views.create_assignment, name='create_assignment'),

    # Submissions
    path('assignments/<int:assignment_id>/submissions/', views.submission_list, name='submission_list'),
    path('submissions/<int:pk>/', views.submission_detail, name='submission_detail'),
    path('assignments/<int:assignment_id>/submissions/create/', views.submission_create, name='submission_create'),
    path('submissions/<int:pk>/update/', views.submission_update, name='submission_update'),
    path('submissions/<int:pk>/delete/', views.submission_delete, name='submission_delete'),

    # Discussions
    path('courses/<int:course_id>/discussions/', views.discussion_list, name='discussion_list'),
    path('discussions/<int:pk>/', views.discussion_detail, name='discussion_detail'),
    path('courses/<int:course_id>/discussions/create/', views.discussion_create, name='discussion_create'),
    path('discussions/<int:pk>/update/', views.discussion_update, name='discussion_update'),
    path('discussions/<int:pk>/delete/', views.discussion_delete, name='discussion_delete'),

    # Notifications
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:pk>/', views.notification_detail, name='notification_detail'),
    path('notifications/create/', views.notification_create, name='notification_create'),
    path('notifications/<int:pk>/update/', views.notification_update, name='notification_update'),
    path('notifications/<int:pk>/delete/', views.notification_delete, name='notification_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

