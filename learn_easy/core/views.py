"""
view de l'applications core
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
<<<<<<< HEAD
from .models import CustomUser, Course, Enrollment, Module, Lesson, Assignment, Submission, Discussion, Notification
from .forms import CustomUserCreationForm
from .forms import CourseForm, ModuleForm, LessonForm, AssignmentForm, SubmissionForm, DiscussionForm, NotificationForm
=======
from .models import CustomUser, Course, Enrollment, Module
from .forms import CustomUserCreationForm, ModuleForm
from .forms import CourseForm
>>>>>>> a65b0c6c78d476ba55391cfa84f19d7545b91a11

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
            return redirect('module_create', course_id=course.id)  # Rediriger vers la création d'un module
    else:
        form = CourseForm()
    return render(request, 'core/course_form.html', {'form': form, 'action': 'Créer'})

<<<<<<< HEAD


# Mise à jour d'un cours (réservée aux professeurs)
=======
# Mise à jour d'un cours (réservée aux professeurs, uniquement pour leurs propres cours)
>>>>>>> a65b0c6c78d476ba55391cfa84f19d7545b91a11
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

<<<<<<< HEAD
# Liste des Modules
@login_required
def module_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    modules = Module.objects.filter(course=course)
    return render(request, 'core/module_list.html', {'course': course, 'modules': modules})

# Détail d'un module
@login_required
def module_detail(request, pk):
    module = get_object_or_404(Module, pk=pk)
    lessons = Lesson.objects.filter(module=module)
    return render(request, 'core/module_detail.html', {'module': module, 'lessons': lessons})

# Création d'un module
@login_required
@user_passes_test(is_professor)
def module_create(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
=======

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
>>>>>>> a65b0c6c78d476ba55391cfa84f19d7545b91a11
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
<<<<<<< HEAD
            module.course = course
            module.save()
            return redirect('lesson_create', module_id=module.id)  # Rediriger vers la création d'une leçon
=======
            module.teacher = request.user  # Associe le cours au professeur connecté
            module.save()
            return redirect('module_list')
>>>>>>> a65b0c6c78d476ba55391cfa84f19d7545b91a11
    else:
        form = ModuleForm()
    return render(request, 'core/module_form.html', {'form': form, 'action': 'Créer'})

<<<<<<< HEAD
# Mise a jour d'un modeule
@login_required
@user_passes_test(is_professor)
def module_update(request, pk):
    module = get_object_or_404(Module, pk=pk)
=======
# Mise à jour d'un cours (réservée aux professeurs, uniquement pour leurs propres cours)
@login_required
@user_passes_test(is_professor)
def module_update(request, pk):
    module = get_object_or_404(Course, pk=pk, teacher=request.user)
>>>>>>> a65b0c6c78d476ba55391cfa84f19d7545b91a11
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
            return redirect('module_detail', pk=module.pk)
=======
            return redirect('course_detail', pk=module.pk)
>>>>>>> a65b0c6c78d476ba55391cfa84f19d7545b91a11
    else:
        form = ModuleForm(instance=module)
    return render(request, 'core/module_form.html', {'form': form, 'action': 'Mettre à jour'})

<<<<<<< HEAD
# Suppression d'un module
@login_required
@user_passes_test(is_professor)
def module_delete(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        module.delete()
        return redirect('module_list', course_id=module.course.id)
    return render(request, 'core/module_confirm_delete.html', {'module': module})

# liste des lessons
@login_required
def lesson_list(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    lessons = Lesson.objects.filter(module=module)
    return render(request, 'core/lesson_list.html', {'module': module, 'lessons': lessons})

# Details d'une leçon
@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    return render(request, 'core/lesson_detail.html', {'lesson': lesson})

# Création d'une leçon
@login_required
@user_passes_test(is_professor)
def lesson_create(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            return redirect('module_detail', pk=module.id)  # Rediriger vers la page de détail du module
    else:
        form = LessonForm()
    return render(request, 'core/lesson_form.html', {'form': form, 'action': 'Créer'})

# Mise à jour d'une leçon
@login_required
@user_passes_test(is_professor)
def lesson_update(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lesson_detail', pk=lesson.pk)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'core/lesson_form.html', {'form': form, 'action': 'Mettre à jour'})

# Suppression d'une leçon
@login_required
@user_passes_test(is_professor)
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        lesson.delete()
        return redirect('lesson_list', module_id=lesson.module.id)
    return render(request, 'core/lesson_confirm_delete.html', {'lesson': lesson})

# Listes des Devoirs
@login_required
def assignment_list(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    assignments = Assignment.objects.filter(module=module)
    return render(request, 'core/assignment_list.html', {'module': module, 'assignments': assignments})

# Détails d'un devoir
@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    return render(request, 'core/assignment_detail.html', {'assignment': assignment})

# Création d'un Devoir
@login_required
@user_passes_test(is_professor)
def assignment_create(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.module = module
            assignment.save()
            return redirect('course_detail', pk=module.course.id)  # Rediriger vers la page de détail du cours
    else:
        form = AssignmentForm()
    return render(request, 'core/assignment_form.html', {'form': form, 'action': 'Créer'})

# Mise à jour d'un Devoir
@login_required
@user_passes_test(is_professor)
def assignment_update(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_detail', pk=assignment.pk)
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'core/assignment_form.html', {'form': form, 'action': 'Mettre à jour'})

# Suppression d'un Devoir
@login_required
@user_passes_test(is_professor)
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignment_list', module_id=assignment.module.id)
    return render(request, 'core/assignment_confirm_delete.html', {'assignment': assignment})

# Listes des soumissions
@login_required
def submission_list(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, 'core/submission_list.html', {'assignment': assignment, 'submissions': submissions})

# Details d'une soumission
@login_required
def submission_detail(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    return render(request, 'core/submission_detail.html', {'submission': submission})

# Création d'une soumission
@login_required
@user_passes_test(is_student)
def submission_create(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.save()
            return redirect('submission_list', assignment_id=assignment.id)
    else:
        form = SubmissionForm()
    return render(request, 'core/submission_form.html', {'form': form, 'action': 'Créer'})

# Mise a jour d'une soumission
@login_required
@user_passes_test(is_student)
def submission_update(request, pk):
    submission = get_object_or_404(Submission, pk=pk, student=request.user)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('submission_detail', pk=submission.pk)
    else:
        form = SubmissionForm(instance=submission)
    return render(request, 'core/submission_form.html', {'form': form, 'action': 'Mettre à jour'})

# Suppression d'une soumission
@login_required
@user_passes_test(is_student)
def submission_delete(request, pk):
    submission = get_object_or_404(Submission, pk=pk, student=request.user)
    if request.method == 'POST':
        submission.delete()
        return redirect('submission_list', assignment_id=submission.assignment.id)
    return render(request, 'core/submission_confirm_delete.html', {'submission': submission})

# Liste des discussions
@login_required
def discussion_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    discussions = Discussion.objects.filter(course=course)
    return render(request, 'core/discussion_list.html', {'course': course, 'discussions': discussions})

# Detail d'une discussion
@login_required
def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    return render(request, 'core/discussion_detail.html', {'discussion': discussion})

# Création d'une discussion
@login_required
def discussion_create(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.course = course
            discussion.user = request.user
            discussion.save()
            return redirect('discussion_list', course_id=course.id)
    else:
        form = DiscussionForm()
    return render(request, 'core/discussion_form.html', {'form': form, 'action': 'Créer'})

# Mise à jour d'une discussion
@login_required
def discussion_update(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            return redirect('discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm(instance=discussion)
    return render(request, 'core/discussion_form.html', {'form': form, 'action': 'Mettre à jour'})

# Suppression d'une discussion
@login_required
def discussion_delete(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk, user=request.user)
    if request.method == 'POST':
        discussion.delete()
        return redirect('discussion_list', course_id=discussion.course.id)
    return render(request, 'core/discussion_confirm_delete.html', {'discussion': discussion})

# Liste des Notifications
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'core/notification_list.html', {'notifications': notifications})

# Détails d'une notification
@login_required
def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return render(request, 'core/notification_detail.html', {'notification': notification})

# Création d'une notification
@login_required
@user_passes_test(is_admin)
def notification_create(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.user = request.user
            notification.save()
            return redirect('notification_list')
    else:
        form = NotificationForm()
    return render(request, 'core/notification_form.html', {'form': form, 'action': 'Créer'})

# Mise a jour d'une notification
@login_required
@user_passes_test(is_admin)
def notification_update(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=notification)
        if form.is_valid():
            form.save()
            return redirect('notification_detail', pk=notification.pk)
    else:
        form = NotificationForm(instance=notification)
    return render(request, 'core/notification_form.html', {'form': form, 'action': 'Mettre à jour'})

# Suppression d'une notification
@login_required
@user_passes_test(is_admin)
def notification_delete(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    if request.method == 'POST':
        notification.delete()
        return redirect('notification_list')
    return render(request, 'core/notification_confirm_delete.html', {'notification': notification})
=======
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
>>>>>>> a65b0c6c78d476ba55391cfa84f19d7545b91a11
