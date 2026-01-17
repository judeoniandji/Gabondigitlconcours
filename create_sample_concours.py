"""
Script pour créer des concours d'exemple avec toutes les informations
"""
import os
import sys
import django
from datetime import date, timedelta

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from concours.models import Concours

# Documents requis standards
DOCUMENTS_STANDARDS = "Demande manuscrite (adressée au ministre), Acte de naissance, Carte d'identité, Casier judiciaire, Certificat médical, Diplômes, Photos d'identité"

# Créer des concours d'exemple
concours_data = [
    {
        'nom': 'Concours d\'entrée dans la Fonction Publique - Catégorie B',
        'description': 'Concours pour le recrutement de fonctionnaires de catégorie B dans les administrations publiques gabonaises. Postes disponibles dans plusieurs ministères.',
        'ministere_organisateur': 'Ministère de la Fonction Publique',
        'niveau_demande': 'Bac',
        'limite_age_min': 18,
        'limite_age_max': 35,
        'nombre_places': 50,
        'date_ouverture': date.today() - timedelta(days=5),
        'date_fermeture': date.today() + timedelta(days=25),
        'lieu_depot': 'En ligne - Plateforme digitale',
        'frais_inscription': 10000,
        'documents_requis': DOCUMENTS_STANDARDS,
        'publie': True,
    },
    {
        'nom': 'Concours d\'entrée à l\'École Nationale d\'Administration (ENA)',
        'description': 'Concours pour l\'admission à l\'École Nationale d\'Administration. Formation de haut niveau pour les cadres supérieurs de l\'État.',
        'ministere_organisateur': 'Ministère de l\'Enseignement Supérieur',
        'niveau_demande': 'Bac+3',
        'limite_age_min': 20,
        'limite_age_max': 30,
        'nombre_places': 30,
        'date_ouverture': date.today() - timedelta(days=10),
        'date_fermeture': date.today() + timedelta(days=30),
        'lieu_depot': 'En ligne - Plateforme digitale',
        'frais_inscription': 15000,
        'documents_requis': DOCUMENTS_STANDARDS,
        'publie': True,
    },
    {
        'nom': 'Concours de recrutement de professeurs des lycées',
        'description': 'Concours pour le recrutement de professeurs certifiés dans les disciplines : Mathématiques, Sciences Physiques, Français, Histoire-Géographie.',
        'ministere_organisateur': 'Ministère de l\'Éducation Nationale',
        'niveau_demande': 'Bac+3',
        'limite_age_min': 22,
        'limite_age_max': 40,
        'nombre_places': 75,
        'date_ouverture': date.today() - timedelta(days=3),
        'date_fermeture': date.today() + timedelta(days=27),
        'lieu_depot': 'En ligne - Plateforme digitale',
        'frais_inscription': 8000,
        'documents_requis': DOCUMENTS_STANDARDS,
        'publie': True,
    },
    {
        'nom': 'Concours d\'entrée dans les Forces de Sécurité',
        'description': 'Recrutement pour les postes de garde de sécurité et agent de police. Formation professionnelle assurée.',
        'ministere_organisateur': 'Ministère de l\'Intérieur',
        'niveau_demande': 'BEPC',
        'limite_age_min': 18,
        'limite_age_max': 28,
        'nombre_places': 100,
        'date_ouverture': date.today() - timedelta(days=7),
        'date_fermeture': date.today() + timedelta(days=23),
        'lieu_depot': 'En ligne - Plateforme digitale',
        'frais_inscription': 5000,
        'documents_requis': DOCUMENTS_STANDARDS,
        'publie': True,
    },
]

def create_concours():
    """Créer les concours d'exemple"""
    import sys
    import io
    # Forcer l'encodage UTF-8 pour Windows
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    created_count = 0
    updated_count = 0
    
    for data in concours_data:
        concours, created = Concours.objects.update_or_create(
            nom=data['nom'],
            defaults=data
        )
        if created:
            created_count += 1
            print(f"Concours cree: {concours.nom}")
        else:
            updated_count += 1
            print(f"Concours mis a jour: {concours.nom}")
    
    print(f"\nResume: {created_count} cree(s), {updated_count} mis a jour")
    print(f"Total de concours dans la base: {Concours.objects.count()}")

if __name__ == '__main__':
    create_concours()
