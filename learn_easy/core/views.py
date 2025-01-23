"""
view de l'applications core
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser, Course, Enrollment, Module
from .forms import CustomUserCreationForm, ModuleForm
from .forms import CourseForm

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


# Liste des cours (accessible par tous les utilisateurs connectés)
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})

# Détail d'un cours
# Détails d'un cours (accessible par tous les utilisateurs connectés)
@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'core/course_detail.html', {'course': course})

# Création d'un cours (réservée aux professeurs)
@login_required
@user_passes_test(is_professor)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user  # Associe le cours au professeur connecté
            course.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'core/course_form.html', {'form': form, 'action': 'Créer'})

# Mise à jour d'un cours (réservée aux professeurs, uniquement pour leurs propres cours)
@login_required
@user_passes_test(is_professor)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'core/course_form.html', {'form': form, 'action': 'Mettre à jour'})

# Suppression d'un cours (réservée aux professeurs, uniquement pour leurs propres cours)
@login_required
@user_passes_test(is_professor)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'core/course_confirm_delete.html', {'course': course})


# Liste des cours (accessible par tous les utilisateurs connectés)
@login_required
def module_list(request):
    modules = Module.objects.all()
    return render(request, 'core/module_list.html', {'modules': modules})

# Détail d'un cours
# Détails d'un cours (accessible par tous les utilisateurs connectés)
@login_required
def module_detail(request, pk):
    module = get_object_or_404(Module, pk=pk)
    return render(request, 'core/module_detail.html', {'module': module})

# Création d'un cours (réservée aux professeurs)
@login_required
@user_passes_test(is_professor)
def module_create(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.teacher = request.user  # Associe le cours au professeur connecté
            module.save()
            return redirect('module_list')
    else:
        form = ModuleForm()
    return render(request, 'core/module_form.html', {'form': form, 'action': 'Créer'})

# Mise à jour d'un cours (réservée aux professeurs, uniquement pour leurs propres cours)
@login_required
@user_passes_test(is_professor)
def module_update(request, pk):
    module = get_object_or_404(Course, pk=pk, teacher=request.user)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=module.pk)
    else:
        form = ModuleForm(instance=module)
    return render(request, 'core/module_form.html', {'form': form, 'action': 'Mettre à jour'})

# Suppression d'un cours (réservée aux professeurs, uniquement pour leurs propres cours)
@login_required
@user_passes_test(is_professor)
def module_delete(request, pk):
    module = get_object_or_404(Module, pk=pk, teacher=request.user)
    if request.method == 'POST':
        module.delete()
        return redirect('module_list')
    return render(request, 'core/module_confirm_delete.html', {'module': module})



# Liste des cours (visible par tout le monde connecté)
# @login_required
# def course_list(request):
#     courses = Course.objects.all()
#     return render(request, 'core/course_list.html', {'courses': courses})

# # Détails d'un cours (visible par tout le monde connecté)
# @login_required
# def course_detail(request, pk):
#     course = get_object_or_404(Course, pk=pk)
#     return render(request, 'core/course_detail.html', {'course': course})

# # Création d'un cours (réservée aux professeurs)
# @login_required
# @user_passes_test(is_professor)
# def course_create(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST, request.FILES)
#         if form.is_valid():
#             course = form.save(commit=False)
#             course.teacher = request.user
#             course.save()
#             return redirect('course_list')
#     else:
#         form = CourseForm()
#     return render(request, 'core/course_form.html', {'form': form, 'action': 'Créer'})

# # Mise à jour d'un cours (réservée aux professeurs)
# @login_required
# @user_passes_test(is_professor)
# def course_update(request, pk):
#     course = get_object_or_404(Course, pk=pk, teacher=request.user)
#     if request.method == 'POST':
#         form = CourseForm(request.POST, request.FILES, instance=course)
#         if form.is_valid():
#             form.save()
#             return redirect('course_detail', pk=course.pk)
#     else:
#         form = CourseForm(instance=course)
#     return render(request, 'core/course_form.html', {'form': form, 'action': 'Mettre à jour'})

# # Suppression d'un cours (réservée aux professeurs)
# @login_required
# @user_passes_test(is_professor)
# def course_delete(request, pk):
#     course = get_object_or_404(Course, pk=pk, teacher=request.user)
#     if request.method == 'POST':
#         course.delete()
#         return redirect('course_list')
#     return render(request, 'core/course_confirm_delete.html', {'course': course})
