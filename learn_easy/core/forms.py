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
    user_type = forms.ChoiceField(
        choices=USER_TYPES, 
        label="Type d'utilisateur",
        widget=forms.Select(attrs={
            'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500'
        })
    )

    class Meta:  
        model = CustomUser  
        fields = ['username', 'password1']  
        widgets = {  
            'username': forms.TextInput(attrs={  
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',  
                'placeholder': 'username'  
            }),  
            'password': forms.PasswordInput(attrs={  
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',  
                'placeholder': 'password'  
            }),   
        }


    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'user_type']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez votre nom d’utilisateur'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez votre prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez votre nom de famille'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Créez un mot de passe'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Confirmez votre mot de passe'
            }),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'teacher']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez un titre'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez une description'
            }),
            # 'teacher': forms.TextInput(attrs={
            #     'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
            #     'placeholder': 'Entrez le nom du professeur'
            # }),
        }

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez un titre'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez une description'
            }),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url', 'pdf_file', 'module']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez un titre'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez le contenu'
            }),
            'video_url': forms.TextInput(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez l\'URL du vidéo'
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Choisissez un fichier PDF'
            }),
            'module': forms.Select(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez le titre du module'
            }),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'module']
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
        #         'placeholder': 'Entrez un titre'
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
        #         'placeholder': 'Entrez une description'
        #     }),
        #     'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'Entrez une date'}),
        #     'module': forms.Select(attrs={
        #         'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
        #         'placeholder': 'Entrez le titre du module'
        #     }),
        # }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez le contenu de la discussion'
            }),
        }

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'w-full border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Entrez le contenu de la discussion'
            }),
        }
        