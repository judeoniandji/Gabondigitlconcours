from rest_framework import serializers
from .models import User, Candidat, Gestionnaire, AuditLog, BugReport, BugEvent

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    nom_complet = serializers.CharField(write_only=True, required=False, allow_blank=True)
    date_naissance = serializers.DateField(write_only=True, required=False)
    lieu_naissance = serializers.CharField(write_only=True, required=False, allow_blank=True)
    ville_naissance = serializers.CharField(write_only=True, required=False, allow_blank=True)
    adresse = serializers.CharField(write_only=True, required=False, allow_blank=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'telephone', 'password', 'is_staff', 'is_superuser', 'is_active', 'nom_complet', 'date_naissance', 'lieu_naissance', 'ville_naissance', 'adresse']
        extra_kwargs = {
            'is_staff': {'read_only': True},
            'is_superuser': {'read_only': True},
        }
    def validate(self, attrs):
        tel = attrs.get('telephone', '')
        role = attrs.get('role')
        if role == 'candidat' and not tel:
            raise serializers.ValidationError({'telephone': 'Téléphone requis pour les candidats'})
        if tel:
            v = str(tel).replace(' ', '')
            import re
            ok = False
            if v.startswith('+'):
                ok = bool(re.fullmatch(r'\+241\d{8}', v))
            else:
                ok = bool(re.fullmatch(r'\d{8}', v))
            if not ok:
                raise serializers.ValidationError({'telephone': 'Format: 8 chiffres ou +241 suivi de 8 chiffres'})
        return attrs
    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.get('role')
        nom_complet = validated_data.pop('nom_complet', '')
        date_naissance = validated_data.pop('date_naissance', None)
        lieu_naissance = validated_data.pop('lieu_naissance', '')
        ville_naissance = validated_data.pop('ville_naissance', '')
        adresse = validated_data.pop('adresse', '')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        active_flag = not (role in ('jury', 'secretaire', 'gestionnaire', 'correcteur', 'president_jury'))
        User._default_manager.filter(pk=user.pk).update(is_active=active_flag)
        if role == 'candidat':
            numero = self._generate_numero_candidat()
            Candidat._default_manager.create(
                user=user,
                nom_complet=nom_complet,
                date_naissance=date_naissance,
                lieu_naissance=lieu_naissance,
                ville_naissance=ville_naissance,
                adresse=adresse,
                numero_candidat=numero,
            )
        elif role in ('gestionnaire', 'jury', 'secretaire'):
            Gestionnaire._default_manager.create(user=user)
        return user

    def _generate_numero_candidat(self):
        import random, time
        from django.utils import timezone
        prefix = f"C{timezone.now().year}"
        for _ in range(10):
            num = f"{prefix}{random.randint(100000, 999999)}"
            from typing import Any
            if not Candidat._default_manager.filter(numero_candidat=num).exists():
                return num
        return f"{prefix}{int(time.time())}"

class CandidatSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Candidat
        fields = ['id', 'user', 'nom_complet', 'date_naissance', 'lieu_naissance', 'ville_naissance', 'adresse', 'document_identite', 'numero_candidat']

class GestionnaireSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Gestionnaire
        fields = ['id', 'user', 'fonction']

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class BugEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugEvent
        fields = ['id', 'bug', 'type', 'detail', 'auteur', 'created_at']

class BugReportSerializer(serializers.ModelSerializer):
    events = BugEventSerializer(many=True, read_only=True)

    class Meta:
        model = BugReport
        fields = ['id', 'titre', 'description', 'etapes', 'environnement', 'severite', 'statut', 'module', 'chemins', 'reporter', 'assigne', 'created_at', 'updated_at', 'events']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data.setdefault('reporter', request.user)
        bug = BugReport._default_manager.create(**validated_data)
        try:
            AuditLog._default_manager.create(acteur=request.user if request and request.user.is_authenticated else None, action='bug_create', ressource='bug', ressource_id=bug.id, payload={'severite': bug.severite, 'statut': bug.statut})
        except Exception:
            pass
        return bug
