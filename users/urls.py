from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CandidatViewSet, GestionnaireViewSet, me, logout_user, AuditLogViewSet, BugReportViewSet, BugEventViewSet
from .token_views import EmailTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'candidats', CandidatViewSet)
router.register(r'gestionnaires', GestionnaireViewSet)
router.register(r'audit', AuditLogViewSet)
router.register(r'bugs', BugReportViewSet)
router.register(r'bug-events', BugEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/email/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair_email'),
    path('me/', me, name='me'),
    path('logout_user/', logout_user, name='logout_user'),
]
