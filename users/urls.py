from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CandidatViewSet, GestionnaireViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'candidats', CandidatViewSet)
router.register(r'gestionnaires', GestionnaireViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
