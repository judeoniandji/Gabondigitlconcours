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
