"""
views de l'application core
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CourseSerializer
from django.shortcuts import render
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Course, CustomUser

from django.contrib.auth.decorators import login_required


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    return render(request, 'core/home.html')


class CourseListAPIView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


@login_required(login_url='/admin/login/')
def dashboard(request):
    if request.user.role == 'teacher':
        total_courses = Course.objects.filter(teacher=request.user).count()
        total_students = CustomUser.objects.filter(role='student').count()
        total_downloads = 120  # Exemple fictif
    else:
        total_courses = Course.objects.count()
        total_students = CustomUser.objects.filter(role='student').count()
        total_downloads = 90  # Exemple fictif

    context = {
        'total_courses': total_courses,
        'total_students': total_students,
        'total_downloads': total_downloads,
    }
    return render(request, 'core/dashboard.html', context)
