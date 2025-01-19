"""
admin de l'application core
"""
from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment, Assignment, Submission, Discussion, Notification

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Discussion)
admin.site.register(Notification)
