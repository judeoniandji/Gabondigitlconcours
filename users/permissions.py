from rest_framework.permissions import BasePermission
from typing import Any

class IsGestionnaireOrAdmin(BasePermission):
    def has_permission(self, request, view) -> Any:
        u = request.user
        return bool(u and u.is_authenticated and (u.is_staff or u.is_superuser or getattr(u, 'role', None) == 'gestionnaire'))

class IsCorrecteur(BasePermission):
    def has_permission(self, request, view) -> Any:
        u = request.user
        return bool(u and u.is_authenticated and getattr(u, 'role', None) == 'correcteur')

class IsPresidentJury(BasePermission):
    def has_permission(self, request, view) -> Any:
        u = request.user
        return bool(u and u.is_authenticated and getattr(u, 'role', None) == 'president_jury')

class IsSecretaireOrAdmin(BasePermission):
    def has_permission(self, request, view) -> Any:
        u = request.user
        return bool(u and u.is_authenticated and (u.is_staff or u.is_superuser or getattr(u, 'role', None) == 'secretaire'))

class IsCandidat(BasePermission):
    def has_permission(self, request, view) -> Any:
        u = request.user
        return bool(u and u.is_authenticated and getattr(u, 'role', None) == 'candidat')