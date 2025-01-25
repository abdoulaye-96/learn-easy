"""
view de l'applications core
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser, Course, Enrollment, Module, Lesson, Discussion, Notification, Assignment
from .forms import CustomUserCreationForm
from .forms import CourseForm, ModuleForm, LessonForm, CourseForm, DiscussionForm, AssignmentForm
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required
def dashboard_view(request):
    # On récupère l'utilisateur connecté
    user = request.user  
    return render(request, 'dashboard.html', {'user': user})

#Fonction pour vérifier le type d'utilisateur
def is_admin(user):
    return user.user_type == 'admin'

def is_professor(user):
    return user.user_type == 'professor'

def is_student(user):
    return user.user_type == 'student'

#Vue tableau de bord principal
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

    #Tableau de bord admin
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = CustomUser.objects.all()
    return render(request, 'core/admin_dashboard.html', {'users': users})

#Tableau de bord professeur
@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'core/professor_dashboard.html', {'courses': courses})

#Tableau de bord étudiant
@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'core/student_dashboard.html', {'enrollments': enrollments})

#Connexion
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

#Déconnexion
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
            login(request, user)
            return redirect('dashboard')
        else:
            # Si le formulaire n'est pas valide, affichez les erreurs sur la même page
            return render(request, 'core/register.html', {'form': form})
    else:
        # Requête GET - affichez le formulaire vide
        form = CustomUserCreationForm()
        return render(request, 'core/register.html', {'form': form})


#Liste des cours (visible par tout le monde connecté)
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})

#Détails d'un cours (visible par tout le monde connecté)
@login_required
# def course_detail(request, pk):
#     course = get_object_or_404(Course, pk=pk)
#     return render(request, 'core/course_detail.html', {'course': course})

# def course_detail(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     modules = course.modules.all()  # Assurez-vous que le modèle Course a une relation avec Module
#     return render(request, 'core/course_detail.html', {
#         'course': course,
#         'modules': modules
#     })
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all()  # Assurez-vous que le modèle Course a une relation avec Module
    return render(request, 'core/course_detail.html', {
        'course': course,
        'modules': modules
    })


#Création d'un cours (réservée aux professeurs)
@login_required
def create_course(request):
    if request.user.user_type != 'professor':
        return HttpResponseForbidden("Vous n'avez pas l'autorisation de créer un cours.")
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()

            # Ajouter plusieurs modules si nécessaire
            module_titles = request.POST.getlist('module_titles')  # Si vous avez une liste de titres de modules
            for title in module_titles:
                Module.objects.create(
                    title=title,
                    course=course,
                )
            return redirect('create_module', course_id=course.id)
    else:
        form = CourseForm()
    return render(request, 'core/course_form.html', {'form': form,'action': 'create'})

@login_required
def add_multiple_lessons(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.user.user_type != 'professor':
        return HttpResponseForbidden("Vous n'avez pas l'autorisation de créer une leçon.")

    if request.method == 'POST':
        # Si vous avez besoin d'ajouter plusieurs leçons en une seule fois
        for lesson_data in request.POST.getlist('lesson_data'):  # Exemple si vous envoyez une liste de leçons
            Lesson.objects.create(
                title=lesson_data['title'],
                content=lesson_data['content'],
                module=module,
            )
        return redirect('module_detail', module.id)
    
    return render(request, 'add_multiple_lessons.html', {'module': module})


#Mise à jour d'un cours (réservée aux professeurs)
@login_required
@user_passes_test(is_professor)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'core/course_form.html', {'form': form, 'action': 'Mettre à jour'})

#Suppression d'un cours (réservée aux professeurs)
@login_required
@user_passes_test(is_professor)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'core/course_confirm_delete.html', {'course': course})

# Listes des modules
@login_required
def module_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    modules = Module.objects.filter(course=course)
    return render(request, 'core/module_list.html', {'course': course, 'modules': modules})

# Details d'un module
@login_required
# def module_detail(request, pk):
#     module = get_object_or_404(Module, pk=pk)
#     return render(request, 'core/module_detail.html', {'module': module})
def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    lessons = module.lessons.all()  # Assurez-vous que le modèle Module a une relation avec Lesson
    assignments = module.assignments.all()
    return render(request, 'core/module_detail.html', {
        'module': module,
        'lessons': lessons,
        'assignments': assignments
    })

# Création d'un module
@login_required
def create_module(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.user_type != 'professor':
        return HttpResponseForbidden("Vous n'avez pas l'autorisation de créer un module.")
    
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            return redirect('create_lesson', module_id=module.id)
    else:
        form = ModuleForm()
    return render(request, 'core/module_form.html', {'form': form, 'action': 'create'})


# Mise à jour d'un module
@login_required
@user_passes_test(is_professor)
def module_update(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('core/module_detail', pk=module.pk)
    else:
        form = ModuleForm(instance=module)
    return render(request, 'core/module_form.html', {'form': form, 'action': 'Mettre à jour'})

# Suppression d'un module
@login_required
@user_passes_test(is_professor)
def module_delete(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        module.delete()
        return redirect('module_list', course_id=module.course.id)
    return render(request, 'core/module_confirm_delete.html', {'module': module})

# Liste des leçons
@login_required
def lesson_list(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    lessons = Lesson.objects.filter(module=module)
    return render(request, 'core/lesson_list.html', {'module': module, 'lessons': lessons})

# Details d'une lesson
@login_required
# def lesson_detail(request, pk):
#     lesson = get_object_or_404(Lesson, pk=pk)
#     return render(request, 'core/lesson_detail.html', {'lesson': lesson})
def lesson_detail(request, lesson_id):
    # lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'core/lesson_detail.html', {'lesson': lesson})


# Création d'une lesson
@login_required
def create_lesson(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    # course = get_object_or_404(Course, id=course_id)
    if request.user.user_type != 'professor':
        return HttpResponseForbidden("Vous n'avez pas l'autorisation de créer une leçon.")
    
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            return redirect('create_assignment', module_id=module.id)  # Utiliser course_id ici
    else:
        form = LessonForm()
    return render(request, 'core/assignment_form.html', {'form': form, 'module': module, 'action': 'create'})



# Mise a jour d'une leçon
@login_required
@user_passes_test(is_professor)
def lesson_update(request, module_id):
    lesson = get_object_or_404(Lesson, id=module_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lesson_detail', id=lesson.id)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'core/lesson_form.html', {'form': form, 'action': 'Mettre à jour'})

@login_required
@user_passes_test(is_professor)
def lesson_delete(request, module_id):
    lesson = get_object_or_404(Lesson, id=module_id)
    if request.method == 'POST':
        lesson.delete()
        return redirect('lesson_list', module_id=lesson.module.id)
    return render(request, 'core/lesson_confirm_delete.html', {'lesson': lesson})

# Listes des devoir
@login_required
def assignment_list(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    assignments = Assignment.objects.filter(module=module)
    return render(request, 'core/assignment_list.html', {'module': module, 'assignments': assignments})

# Details d'un devoir
@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    return render(request, 'core/assignment_detail.html', {'assignment': assignment})

# Création d'un devoir
@login_required
def create_assignment(request, module_id, course_id):
    if request.user.user_type != 'professor':
        return HttpResponseForbidden("Vous n'avez pas l'autorisation de créer un devoir.")
    
    module = get_object_or_404(Module, id=module_id)
    course = get_object_or_404(course, id=course_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.module = module
            assignment.save()
            return redirect('course_detail', module_id=module.id, course_id=course.id)
    else:
        form = AssignmentForm()
    return render(request, 'core/assignment_form.html', {'form': form, 'module': module, 'action': 'create'})


# Mise a jour d'un devoir
@login_required
@user_passes_test(is_professor)
def assignment_update(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_detail', module_id=assignment.module.id)
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'core/assignment_form.html', {'form': form, 'action': 'Mettre à jour'})

# Suppression d'un devoir
@login_required
@user_passes_test(is_professor)
def assignment_delete(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    module_id = assignment.module.id
    assignment.delete()
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignment_list', module_id=assignment.module.id)
    return render(request, 'core/assignment_confirm_delete.html', {'assignment': assignment})

# Listes des soumissions
@login_required
def submission_list(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
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

# Suppression
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

# Details d'une discussion
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

# Mise a jour d'une discussion
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

# Listes des notifications
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'core/notification_list.html', {'notifications': notifications})

# Details d'une notification
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

# Suppression d'une notificationaaaa
@login_required
@user_passes_test(is_admin)
def notification_delete(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    if request.method == 'POST':
        notification.delete()
        return redirect('notification_list')
    return render(request, 'core/notification_confirm_delete.html', {'notification': notification})

@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user not in course.students.all():
        course.students.add(request.user)  # Ajoute l'utilisateur connecté au cours
    return redirect('course_detail', course_id=course_id)

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    if course.students.filter(id=user.id).exists():
        messages.info(request, "Vous êtes déjà inscrit à ce cours.")
    else:
        course.students.add(user)
        messages.success(request, "Inscription réussie au cours !")
    return redirect('course_detail', course_id=course_id)

@login_required
def my_courses(request):
    courses = request.user.enrolled_courses.all()  # Récupère les cours de l'utilisateur connecté
    return render(request, 'courses/my_courses.html', {'courses': courses})
