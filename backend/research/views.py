from rest_framework import viewsets
from .serializers import (
    ProjectSerializer,
    PublicationSerializer,
)
from .models import Project, Publication
from users.permissions import IsFaculty, IsHoD, IsResearchScholar, IsStudent


class ProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        # TODO: HOD should be able to see all
        return Project.objects.filter(authors=self.request.user)


class PublicationView(viewsets.ModelViewSet):
    serializer_class = PublicationSerializer

    def get_queryset(self):
        # TODO: HOD should be able to see all
        return Publication.objects.filter(authors=self.request.user)
