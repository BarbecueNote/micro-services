# TP MIXTE

Ce dépôt contient une collection de microservices pour la gestion d'un système de réservation de films. Chaque service est conçu pour gérer une partie spécifique du système, assurant une architecture modulaire et évolutive.

## _Service de réservation (Booking)_

Ce service permet de récupérer la liste de toutes les réservations, de consulter toutes les réservations associées à un utilisateur spécifique et d'ajouter une réservation à un utilisateur.

## _Service de films (Movie)_

Ce service permet de trouver un film par son nom ou son identifiant, de mettre à jour la note ou le nom d'un film, d'ajouter un nouveau film au système, de supprimer un film et de récupérer la liste des acteurs d'un film.

## _Service de séances (Showtime)_

Ce service offre la fonctionnalité d'afficher une liste de tous les films ainsi que leurs horaires de projection et permet de filtrer les films projetés à une date spécifique.

## _Service utilisateur (User)_

Ce service gère les opérations liées aux utilisateurs, telles que la création et la gestion des profils d'utilisateurs au sein du système.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :
- [Git](https://git-scm.com)
- [Python](https://www.python.org/)
- [Pip](https://pypi.org/project/pip/)
- [Docker](https://www.docker.com/)

Les versions spécifiques des dépendances sont listées dans le fichier `requirements.txt`.

## Comment démarrer

Pour lancer un service spécifique, suivez ces étapes :

```bash
# Cloner le projet
git clone https://github.com/BarbecueNote/micro-services

# Accéder au répertoire du projet
cd UE-AD-A1-REST-main

# Installer les dépendances
pip install -r requirements.txt

# Lancer un microservice spécifique (par exemple, le service de films)
cd movie
python movie.py
# En mode développement, vous pouvez utiliser :
pymon movie.py

# Le service de films sera initialisé à l'adresse <http://localhost:3200>
```
## Conteneurisation de l'application
Pour créer et lancer les conteneurs Docker, utilisez les commandes suivantes :
```bash
# Création des images Docker
docker build -t nom_de_votre_service .

# Lancement des conteneurs
docker-compose up
```
## Contributeurs
Julien DAE & Mouad KERARA
