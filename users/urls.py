from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CandidatViewSet, GestionnaireViewSet
from .authentication import EmailTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'candidats', CandidatViewSet)
router.register(r'gestionnaires', GestionnaireViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/email/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair_email'),
]
