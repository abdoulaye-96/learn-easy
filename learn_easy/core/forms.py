from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Course


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
