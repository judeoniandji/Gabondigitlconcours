<<<<<<< HEAD
# Digitalisation des Concours Administratifs du Gabon

## Structure du projet

- Backend Django REST Framework (API, sécurité, logique métier)
- Frontend React (UI, formulaires, dashboard)
- PostgreSQL (base de données)

## Installation backend

1. Créer un environnement virtuel Python
2. Installer les dépendances :
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Configurer `.env` à partir de `.env.example` (clés Airtel, Mailgun, Twilio)
4. Appliquer les migrations :
   ```bash
   python manage.py migrate
   ```
5. Lancer le serveur :
   ```bash
   python manage.py runserver
   ```

## Installation frontend

1. Aller dans `frontend/`
2. Installer les dépendances :
   ```bash
   npm install
   ```
3. Lancer l’application :
   ```bash
   npm start
   ```

## Fonctionnalités principales
- Inscription/connexion (JWT)
- Paiement en ligne Airtel Money (sandbox)
- Validation/rejet dossiers
- Génération convocation
- Notifications mail/SMS
- Dashboard admin/statistiques
- Publication résultats en ligne

## Sécurité
- Hashage bcrypt, permissions par rôle
- Logs Django (fichier `django.log`)
- Préparation sauvegardes

## APIs intégrées
- Airtel Money Sandbox (paiement)
- Mailgun (emails)
- Twilio (SMS)

## Pour aller plus loin
- Ajouter d’autres moyens de paiement
- Statistiques avancées, export PDF/Excel
- API mobile

---
Pour toute question, consulter la documentation dans le dossier `docs/` ou contacter l’équipe technique.

```
digital-concours/
│
├── backend/           # Django REST (API, logique, models, sécurité)
│   ├── backend/       # Projet Django principal (settings, urls)
│   ├── users/         # Authentification, rôles
│   ├── concours/      # Gestion concours
│   ├── payments/      # Paiement Airtel Money
│   ├── notifications/ # Emails, SMS
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

## Initialisation réalisée
- Backend Django REST Framework prêt (apps : users, concours, payments, notifications)
- Frontend React créé (structure de base)

## Prochaine étape
Configurer la base de données PostgreSQL et connecter le backend.

---

Pour toute question ou pour démarrer le développement métier, lance la prochaine étape ou demande un focus sur un point précis.
=======
# Gabondigitlconcours
>>>>>>> a7439b0531a045ec454c94e45cc2c13331556afd
