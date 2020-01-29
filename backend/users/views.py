from rest_framework import viewsets
from .serializers import (
    DepartmentSerializer,
    FacultySerializer,
    StudentSerializer,
    ResearchScholarSerializer,
)
from .models import Department, Faculty, Student, ResearchScholar


class ResearchScholarView(viewsets.ModelViewSet):
    serializer_class = ResearchScholarSerializer

    def get_queryset(self):
        return ResearchScholar.objects.filter(dept=self.request.user.dept)


class DepartmentView(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.all()


class FacultyView(viewsets.ModelViewSet):
    serializer_class = FacultySerializer

    def get_queryset(self):
        return Faculty.objects.filter(dept=self.request.user.dept)


class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.all()
