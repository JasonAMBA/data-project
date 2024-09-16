# Credit Scoring project

## Description
Embauché en tant que Consultant data au sein de Home Credit, l'objectif etait de développer un modèle de credit scoring et le mettre en production.

# ## Structure du Repo
- `notebooks/`: Contient le notebook Python expliquant la démarche, le nettoyage des données et la modélisation.
- `notebook_credit_scoring_model`: Contient le notebook pour le développement du modèle
- `notebook_merged_data`: Contient le notebook pour la fusion des données.
- `src/api/`: Code pour déployer le modèle sous forme d’API.
- `src/dashboard/`: Code pour générer le dashboard interactif.
- `data/uncleaned data`: Données brutes.
- `data/cleaned data`: Données nettoyés.
- `requirements.txt`: Liste des dépendances Python nécessaires.
- `.gitignore`: Liste des fichiers et dossiers à ignorer dans Git.

##
Dans un premier temps, il faut d'abord télécharger le jeu de données complet en cliquant sur ce lien : https://drive.google.com/uc?export=download&id=1-KMviSMps_3L6WXciwq7KMvL7m0SGNK3

Après avoir téléchargé le jeu de données complet, il faudra le mettre sur le répertoire du projet

## Installation
1. Clonez le repo :

2. Accédez au répertoire du projet :

3. Installez les dépendances : Dans le répertoire du projet, taper : "pip install -r requirements.txt"

4. Mettre le jeu de donnée sur le répertoire du projet

## Utilisation
### Lancer l'API
Pour lancer l'API localement, il faut taper dans le terminal : "cd src/api", puis taper "python app.py"

### Lancer le Dashboard
Pour lancer le dashboard localement, il faut d'abord lancer l'api localement dans un terminal. Ensuite, il faudra taper dans un autre terminal "cd src/dashboard", puis taper python dashboard.py
