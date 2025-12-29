from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from django.utils import timezone
from .models import User, Candidat, Gestionnaire, AuditLog, BugReport, BugEvent
from .serializers import UserSerializer, CandidatSerializer, GestionnaireSerializer, AuditLogSerializer, BugReportSerializer, BugEventSerializer

def login_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST["username"]  # Peut être un email
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # À adapter selon votre projet
        else:
            error = "Identifiants invalides"
    return render(request, "login.html", {"error": error})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User._default_manager.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        role = request.data.get('role')
        is_admin = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
        if role != 'candidat' and not is_admin:
            return Response({'detail': 'Création limitée aux candidats. Créez les autres comptes via un admin.'}, status=403)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        try:
            if role != 'candidat':
                user.is_active = False
                user.save(update_fields=['is_active'])
            AuditLog._default_manager.create(acteur=request.user if request.user.is_authenticated else None, action='user_create', ressource='user', ressource_id=user.id, payload={'role': role})
        except Exception:
            pass
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    @action(detail=True, methods=['put'], permission_classes=[IsAdminUser])
    def activate(self, request, pk=None):
        u = self.get_object()
        u.is_active = True
        u.save(update_fields=['is_active'])
        try:
            AuditLog._default_manager.create(acteur=request.user, action='user_activate', ressource='user', ressource_id=u.id, payload={'username': u.username})
        except Exception:
            pass
        return Response({'detail': 'Compte activé'})

class CandidatViewSet(viewsets.ModelViewSet):
    queryset = Candidat._default_manager.all()
    serializer_class = CandidatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class GestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Gestionnaire._default_manager.all()
    serializer_class = GestionnaireSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def logout_user(request):
    user_id = request.data.get('user_id')
    u_qs = User._default_manager.filter(id=user_id)
    if not u_qs.exists():
        return Response({'detail': 'Utilisateur introuvable'}, status=404)
    u = u_qs.first()
    u.token_valid_after = timezone.now()
    u.save(update_fields=['token_valid_after'])
    try:
        AuditLog._default_manager.create(acteur=request.user, action='user_logout_force', ressource='user', ressource_id=u.id, payload={'username': u.username})
    except Exception:
        pass
    return Response({'detail': 'Utilisateur déconnecté'})

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog._default_manager.order_by('-created_at')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]

class BugReportViewSet(viewsets.ModelViewSet):
    queryset = BugReport._default_manager.order_by('-created_at')
    serializer_class = BugReportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'assign', 'change_status']:
            return [IsAdminUser()]
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=True, methods=['put'], permission_classes=[IsAdminUser])
    def assign(self, request, pk=None):
        bug = self.get_object()
        assigne_id = request.data.get('assigne_id')
        assigne_qs = User._default_manager.filter(id=assigne_id)
        bug.assigne = assigne_qs.first() if assigne_qs.exists() else None
        bug.save(update_fields=['assigne'])
        BugEvent._default_manager.create(bug=bug, type='assign', detail=str(assigne_id), auteur=request.user)
        try:
            AuditLog._default_manager.create(acteur=request.user, action='bug_assign', ressource='bug', ressource_id=bug.id, payload={'assigne_id': assigne_id})
        except Exception:
            pass
        return Response({'detail': 'Assigné'})

    @action(detail=True, methods=['put'], permission_classes=[IsAdminUser])
    def change_status(self, request, pk=None):
        bug = self.get_object()
        statut = request.data.get('statut')
        bug.statut = statut
        bug.save(update_fields=['statut'])
        BugEvent._default_manager.create(bug=bug, type='status', detail=statut, auteur=request.user)
        try:
            AuditLog._default_manager.create(acteur=request.user, action='bug_status', ressource='bug', ressource_id=bug.id, payload={'statut': statut})
        except Exception:
            pass
        return Response({'detail': 'Statut mis à jour'})

class BugEventViewSet(viewsets.ModelViewSet):
    queryset = BugEvent._default_manager.order_by('-created_at')
    serializer_class = BugEventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        bug_id = request.data.get('bug')
        type_ = request.data.get('type')
        detail = request.data.get('detail')
        bug_qs = BugReport._default_manager.filter(id=bug_id)
        if not bug_qs.exists():
            return Response({'detail': 'Bug introuvable'}, status=404)
        ev = BugEvent._default_manager.create(bug=bug_qs.first(), type=type_, detail=detail or '', auteur=request.user if request.user.is_authenticated else None)
        try:
            AuditLog._default_manager.create(acteur=request.user if request.user.is_authenticated else None, action='bug_event', ressource='bug', ressource_id=bug_id, payload={'type': type_})
        except Exception:
            pass
        return Response(BugEventSerializer(ev).data)
