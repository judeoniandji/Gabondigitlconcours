from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConcoursViewSet, DossierViewSet, ResultatViewSet, SerieViewSet, MatiereViewSet, NoteViewSet

router = DefaultRouter()
router.register(r'concours', ConcoursViewSet)
router.register(r'dossiers', DossierViewSet)
router.register(r'resultats', ResultatViewSet)
router.register(r'series', SerieViewSet)
router.register(r'matieres', MatiereViewSet)
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
