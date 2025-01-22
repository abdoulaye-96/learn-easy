"""
models de l'application core
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Administrateur'),
        ('professor', 'Professeur'),
        ('student', 'Étudiant'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')

    # Ajout des related_name uniques
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Nouveau nom unique
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Nouveau nom unique
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

# Modèle de cours
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'professor'},
        related_name='teacher_courses',
        default=1
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ('can_manage_courses', 'Can manage courses'),
            ('can_view_courses', 'Can view courses'),
        ]


# Modèle de module
class Module(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"

# Modèle de leçon
class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='lessons/pdfs/', blank=True, null=True)
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.module.title})"

# Modèle d'inscription
class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'student'},
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"

# Modèle de devoir
class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    def __str__(self):
        return f"{self.title} ({self.module.title})"

# Modèle de soumission
class Submission(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'student'},
        related_name='submissions'
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.assignment.title} - {self.student.username}"

# Modèle de discussion
class Discussion(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='discussions'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Discussion by {self.user.username} in {self.course.title}"

# Modèle de notification
class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
