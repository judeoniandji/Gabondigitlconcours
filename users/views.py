from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from .models import User, Candidat, Gestionnaire
from .serializers import UserSerializer, CandidatSerializer, GestionnaireSerializer

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
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CandidatViewSet(viewsets.ModelViewSet):
    # Eager load the related User object to prevent N+1 queries.
    # This significantly improves performance by reducing the number of database queries
    # from N+1 to just one, where N is the number of candidates.
    queryset = Candidat.objects.select_related('user').all()
    serializer_class = CandidatSerializer

class GestionnaireViewSet(viewsets.ModelViewSet):
    # Eager load the related User object to prevent N+1 queries.
    # This significantly improves performance by reducing the number of database queries
    # from N+1 to just one, where N is the number of managers.
    queryset = Gestionnaire.objects.select_related('user').all()
    serializer_class = GestionnaireSerializer
