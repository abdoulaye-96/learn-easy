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
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'user_type']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'teacher']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url', 'pdf_file', 'module']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'module']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

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