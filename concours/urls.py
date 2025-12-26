from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConcoursViewSet, DossierViewSet, ResultatViewSet

router = DefaultRouter()
router.register(r'concours', ConcoursViewSet)
router.register(r'dossiers', DossierViewSet)
router.register(r'resultats', ResultatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
