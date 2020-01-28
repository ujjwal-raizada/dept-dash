from django.urls import path, include
from rest_framework import routers
from .views import PublicationView, ProjectView

router = routers.DefaultRouter()
router.register(r'publications', PublicationView, 'publications')
router.register(r'projects', ProjectView, 'projects')

urlpatterns = [
    path("", include(router.urls))
]
