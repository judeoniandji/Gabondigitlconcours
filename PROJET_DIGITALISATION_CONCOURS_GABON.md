# Digitalisation des Concours Administratifs du Gabon

## Objectif
Automatiser et sécuriser tout le processus d’inscription, de paiement, de gestion et de suivi des concours administratifs au Gabon, via une plateforme web moderne (hors épreuves écrites).

---

## 1. Utilisateurs
- **Candidats** : inscription, paiement, suivi, convocation, résultats
- **Gestionnaires** (admin, jury, secrétaire) : création/gestion concours, validation dossiers, statistiques

## 2. Fonctionnalités clés
- Création de compte candidat (infos personnelles, documents)
- Paiement en ligne obligatoire via Airtel Money (API)
- Validation/rejet dossiers par gestionnaires
- Génération automatique de convocations
- Notifications automatiques mail/SMS
- Tableau de bord admin/statistiques
- Publication des résultats en ligne

## 3. Architecture technique
- **Backend** : Django REST Framework (Python)
- **Frontend** : React.js (JavaScript)
- **Base de données** : PostgreSQL
- **Sécurité** : HTTPS, hash mots de passe, logs, sauvegardes
- **API externes** : Airtel Money (paiement), Mail/SMS (notifications)
- **Pattern** : MVC strict (backend), découplage frontend/backend (API REST)

### Structure projet
```
digital-concours/
│
├── backend/           # Django REST (API, logique, models, sécurité)
│   ├── concours/      # App concours (models, views, serializers, urls)
│   ├── users/         # Authentification, rôles
│   ├── payments/      # Paiement Airtel Money
│   ├── notifications/ # Emails, SMS
│   ├── settings.py    # Config
│   └── ...
│
├── frontend/          # React (UI, formulaires, dashboard)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/  # API, auth, paiement
│   │   └── ...
│   └── package.json
│
├── docs/              # Documentation
└── README.md
```

## 4. MVP (Produit minimum viable)
- Inscription + téléversement document
- Paiement Airtel Money (API)
- Validation dossiers
- Génération convocation
- Dashboard gestionnaire
- Notifications mail/SMS
- Résultats en ligne

## 5. Sécurité & conformité
- Authentification JWT
- Permissions par rôle
- Hashage des mots de passe (bcrypt)
- Logs et audit transactions
- Sauvegardes automatiques

## 6. APIs gratuites à intégrer
- **Airtel Money Sandbox** (paiement) : https://developer.airtel.africa/docs/
- **Mailgun (free tier)** (mail) : https://www.mailgun.com/pricing/
- **Twilio (free tier)** (SMS) : https://www.twilio.com/sms/pricing

## 7. Bonnes pratiques
- Code commenté, structuré, évolutif
- Modularité backend/frontend
- Documentation technique fournie
- Prêt pour montée en charge (scalabilité)

## 8. Workflow simplifié
INSCRIPTION → VALIDATION DOSSIER → PAIEMENT → VALIDATION ADMIN → CONVOCATION → COMPOSITION PHYSIQUE → RESULTATS EN LIGNE

---

## Pour aller plus loin
- Ajout d’autres moyens de paiement
- Génération automatique de statistiques avancées
- Export PDF/Excel des listes
- API mobile

---

## Avancées réalisées (Jan 2026)
- Backend lancé en développement: `http://127.0.0.1:8000/` (Django) 
- Authentification JWT opérationnelle: `POST /api/token/`, `POST /api/users/token/email/` 
- RBAC implémenté côté API: candidats, gestionnaires, jury, secrétaire, correcteur, président de jury 
- Modèles concours enrichis: séries, matières, notes, statut publication des résultats, lien Dossier-Série
- Routes sécurisées et filtrage:
  - `GET/POST /api/concours/concours/` (filtre `?ouvert=true`) 
  - `GET/POST /api/concours/series/`, `matieres/`, `notes/` 
  - `PUT /api/concours/notes/{id}/valider/` (président de jury) 
  - `PUT /api/concours/concours/{id}/publier/` (publication officielle) 
  - `GET /api/concours/matieres/{id}/candidats/` (anonymisé pour jury)
  - `GET /api/concours/series/{id}/classement/` (anonymisé pour délibération)
- Journalisation des actions (AuditLog): activation utilisateurs, validation notes, publication concours 
- Interface React:
  - Menu admin avec liens rapides (API, Swagger, gestion) 
  - Page "Explorateur API Admin" pour tester les endpoints avec JWT 
  - Page "Gestion des profils" (CRUD utilisateurs, rôles, activation staff) 
  - Sélecteur d’espace par rôle (Candidat/Jury/Secrétaire/Gestion) 
  - **Portail Candidat**: Sélection de concours et série, soumission dossier, suivi statut
  - **Portail Jury**: 
    - Saisie des notes par matière avec anonymat (numéro candidat)
    - Distinction Correcteur (saisie) vs Président (saisie + validation)
    - Onglet "Délibération" pour le Président (classement anonyme par moyenne)
- Anonymat respecté: Les correcteurs et le président voient uniquement le `numero_candidat` (généré à la validation du dossier), jamais l'identité de l'utilisateur.
- Déconnexion forcée d’un utilisateur: `POST /api/users/logout_user/` (révocation JWT) 
- Paiement Airtel: endpoints et client prêts pour sandbox 

## Vérifications effectuées (E2E)
- Création concours → série → matières → inscription candidat (avec choix série) → validation dossier (génération numéro) → saisie des notes par correcteur → validation par président → classement par série → publication 
- Exemple de classement sérialisé: moyenne calculée et anonymat respecté (numéro candidat) 
- Tests unitaires backend: couverture du flux jury et anonymat (`concours.tests`)

## Instructions de lancement (dev)
- Variables: `DB_USE_SQLITE=True` (SQLite dev) 
- Démarrer: `python manage.py runserver` 
- Swagger: `http://127.0.0.1:8000/swagger/` 
- Frontend (si lancé): `http://localhost:3000/` 

## Accès & Comptes (dev)
- Frontend (site): `http://localhost:3000/`
  - Connexion générale: `/`
  - Inscription: `/register`
  - Connexions par rôle: `/login/candidat`, `/login/jury`, `/login/secretaire`, `/login/gestion`, `/login/correcteur`, `/login/president`
- Backend (API & Admin): `http://127.0.0.1:8000/`
  - Admin Django: `/admin/`
  - Jeton par identifiant: `POST /api/token/` (voir [urls.py](file:///c:/Users/KURTIS/CascadeProjects/digital-concours/backend/urls.py#L39-L51))
  - Jeton par email: `POST /api/users/token/email/` (voir [users/urls.py](file:///c:/Users/KURTIS/CascadeProjects/digital-concours/users/urls.py#L14-L19), [token_views.py](file:///c:/Users/KURTIS/CascadeProjects/digital-concours/users/token_views.py#L7-L26))

### Créer un compte administrateur (superuser)
Exécuter dans le dossier du projet:
```
python manage.py createsuperuser
```
Alternative (script existant): `python create_superuser.py` (voir [create_superuser.py](file:///c:/Users/KURTIS/CascadeProjects/digital-concours/create_superuser.py))

### Créer un compte candidat (UI)
Aller sur `http://localhost:3000/register` et remplir les champs obligatoires:
- username, email, password
- role = `candidat`
- telephone (format: 8 chiffres ou `+241` suivi de 8 chiffres)

Règle de validation téléphone côté API (voir [users/serializers.py](file:///c:/Users/KURTIS/CascadeProjects/digital-concours/users/serializers.py#L18-L33)).

### Créer un compte via API
Endpoint: `POST http://127.0.0.1:8000/api/users/users/`

Body JSON minimal pour candidat:
```json
{
  "username": "cand_demo",
  "email": "cand@example.com",
  "password": "Pass123!",
  "role": "candidat",
  "telephone": "+24112345678"
}
```
Remarques:
- Les rôles non-candidats (jury, secrétaire, gestion, correcteur, président) doivent être créés par un admin; ils ne sont pas activés automatiquement (voir [users/views.py](file:///c:/Users/KURTIS/CascadeProjects/digital-concours/users/views.py#L36-L53)).
- Après création, l’authentification se fait via `POST /api/token/` (identifiant) ou `POST /api/users/token/email/` (email). La réponse contient `access` et `refresh`.

### Jetons & Intercepteur Frontend
Le frontend n’envoie pas d’Authorization pour l’inscription et la connexion afin d’éviter l’erreur JWT (“Given token not valid…”). Voir [api.js](file:///c:/Users/KURTIS/CascadeProjects/digital-concours/frontend/src/services/api.js#L9-L15).

## Prochaines étapes
- Paramètres de production (PostgreSQL, CORS/CSRF, https)
- Tests automatiques frontend CI lint/typecheck
