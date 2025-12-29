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

## Avancées réalisées (Déc 2025)
- Backend lancé en développement: `http://127.0.0.1:8000/` (Django) 
- Authentification JWT opérationnelle: `POST /api/token/`, `POST /api/users/token/email/` 
- RBAC implémenté côté API: candidats, gestionnaires, jury, secrétaire, correcteur, président de jury 
- Modèles concours enrichis: séries, matières, notes, statut publication des résultats 
- Routes sécurisées et filtrage:
  - `GET/POST /api/concours/concours/` (filtre `?ouvert=true`) 
  - `GET/POST /api/concours/series/`, `matieres/`, `notes/` 
  - `PUT /api/concours/notes/{id}/valider/` (président de jury) 
  - `PUT /api/concours/concours/{id}/publier/` (publication officielle) 
- Journalisation des actions (AuditLog): activation utilisateurs, validation notes, publication concours 
- Interface React d’administration:
  - Menu admin avec liens rapides (API, Swagger, gestion) 
  - Page "Explorateur API Admin" pour tester les endpoints avec JWT 
  - Page "Gestion des profils" (CRUD utilisateurs, rôles, activation staff) 
  - Sélecteur d’espace par rôle (Candidat/Jury/Secrétaire/Gestion) 
- Déconnexion forcée d’un utilisateur: `POST /api/users/logout_user/` (révocation JWT) 
- Paiement Airtel: endpoints et client prêts pour sandbox 

## Vérifications effectuées (E2E)
- Création concours → série → matières → inscription candidat → saisie des notes par correcteur → validation par président → classement par série → publication 
- Exemple de classement sérialisé: moyenne calculée et anonymat respecté (numéro candidat) 

## Instructions de lancement (dev)
- Variables: `DB_USE_SQLITE=True` (SQLite dev) 
- Démarrer: `python manage.py runserver` 
- Swagger: `http://127.0.0.1:8000/swagger/` 
- Frontend (si lancé): `http://localhost:3001/` 

## Prochaines étapes
- UI jury: saisie/édition par matière, validation par président 
- Masquage des identités côté jury/correcteurs dans toutes les réponses 
- Tests automatiques DRF et CI lint/typecheck 
- Paramètres de production (PostgreSQL, CORS/CSRF, https)
