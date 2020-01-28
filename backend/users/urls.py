from django.urls import path, include
from rest_framework import routers
from .views import FacultyView, ResearchScholarView


router = routers.DefaultRouter()
router.register(r'faculties', FacultyView, 'faculty')
router.register(r'scholars', ResearchScholarView, 'scholar')

urlpatterns = [
    path("", include(router.urls))
]
