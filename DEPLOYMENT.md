# Guide de Déploiement - Plateforme Concours Gabon

## Option 1 : Développement Local (Déjà configuré)

Si vous développez sur votre machine, vous n'avez pas besoin de Docker. Utilisez simplement les terminaux existants :

- **Frontend** : http://localhost:3000 (lancé via `npm start`)
- **Backend** : http://127.0.0.1:8000 (lancé via `python manage.py runserver`)

## Option 2 : Déploiement Docker (Production)

Ce projet est aussi configuré pour être déployé facilement avec Docker et Docker Compose.

### Prérequis

- **Docker Desktop installé et lancé** (Obligatoire pour cette méthode)
- Git

### Structure de Déploiement

Le déploiement utilise 3 conteneurs orchestrés :
1. **Frontend (Nginx)** : Sert l'application React et agit comme proxy inverse pour l'API.
2. **Backend (Django/Gunicorn)** : API REST.
3. **Database (PostgreSQL)** : Base de données de production.

## Étapes de Déploiement Rapide

1. **Cloner le projet** (si ce n'est pas déjà fait)
2. **Lancer avec Docker Compose** :

```bash
docker-compose up -d --build
```

3. **Accéder à l'application** :
   - Ouvrez votre navigateur sur `http://localhost`

## Commandes Utiles

- **Voir les logs** :
  ```bash
  docker-compose logs -f
  ```

- **Arrêter les services** :
  ```bash
  docker-compose down
  ```

- **Créer un superutilisateur (Admin)** :
  ```bash
  docker-compose exec backend python manage.py createsuperuser
  ```

## Configuration de Production

Pour un déploiement réel sur un serveur (AWS, DigitalOcean, VPS) :

1. **Variables d'environnement** :
   - Modifiez `docker-compose.yml` pour définir des mots de passe sécurisés (`POSTGRES_PASSWORD`, `DB_PASSWORD`, `DJANGO_SECRET_KEY`).
   - Ne committez jamais les mots de passe réels dans Git. Utilisez un fichier `.env` non versionné.

2. **Domaine et HTTPS** :
   - En production, il faudra configurer HTTPS (SSL/TLS).
   - Modifiez `frontend/nginx.conf` pour inclure les certificats SSL.

3. **Backup** :
   - Mettez en place des sauvegardes régulières du volume `postgres_data`.

## Dépannage

- Si le backend ne démarre pas, vérifiez que la base de données est prête (`docker-compose logs db`).
- Si les fichiers statiques (CSS Admin) ne chargent pas, forcez la collecte :
  ```bash
  docker-compose exec backend python manage.py collectstatic --noinput
  ```
