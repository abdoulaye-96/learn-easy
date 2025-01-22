"""
view de l'applications core
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser, Course, Enrollment
from .forms import CustomUserCreationForm

# Fonction pour vérifier le type d'utilisateur
def is_admin(user):
    return user.user_type == 'admin'

def is_professor(user):
    return user.user_type == 'professor'

def is_student(user):
    return user.user_type == 'student'

# Vue tableau de bord principal
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'admin':
            return redirect('admin_dashboard')
        elif request.user.user_type == 'professor':
            return redirect('professor_dashboard')
        elif request.user.user_type == 'student':
            return redirect('student_dashboard')
    # Page générique pour les utilisateurs non connectés
    return render(request, 'core/dashboard.html', {
        'message': "Bienvenue sur la plateforme ! Connectez-vous ou inscrivez-vous pour accéder à plus de fonctionnalités."
    })


# Tableau de bord admin
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = CustomUser.objects.all()
    return render(request, 'core/admin_dashboard.html', {'users': users})

# Tableau de bord professeur
@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'core/professor_dashboard.html', {'courses': courses})

# Tableau de bord étudiant
@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'core/student_dashboard.html', {'enrollments': enrollments})

# Connexion
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Connecte l'utilisateur
            return redirect('dashboard')  # Redirection après connexion
        else:
            return render(request, 'core/login.html', {
                'form': form,
                'error': "Nom d'utilisateur ou mot de passe incorrect."
            })
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# Déconnexion
def logout_view(request):
    logout(request)
    return redirect('login')

# Inscription
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = form.cleaned_data['user_type']  # Inscription par défaut comme étudiant
            user.save()
            # return redirect('login') 
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})
