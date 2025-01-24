from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Course, Module, Lesson, Assignment, Submission, Discussion, Notification


class CustomUserCreationForm(UserCreationForm):
    USER_TYPES = (
        ('admin', 'Administrateur'),
        ('professor', 'Professeur'),
        ('student', 'Étudiant'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPES, label="Type d'utilisateur")

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'user_type']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'teacher', 'pdf_file', 'video_url']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url', 'pdf_file']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['content']

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message']
