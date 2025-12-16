# Scraping Free-Work - Extraction d'offres d'emploi IT

## Description du projet

Ce projet permet d'extraire automatiquement des offres d'emploi depuis le site Free-Work.com afin de constituer un dataset d'analyse pour l'atelier d'analyse de donnees.

## Fonctionnalites

- Connexion ethique au site avec User-Agent approprie
- Extraction automatique des offres d'emploi (titre, entreprise, salaire, description)
- Gestion de la pagination pour parcourir plusieurs pages
- Robustesse avec gestion des erreurs (try/except)
- Rate limiting (pauses entre les requetes)
- Export des donnees en CSV avec Pandas

## Prerequis

- Python 3.x
- Environnement virtuel (venv)
- Bibliotheques Python :
  - requests (pour les requetes HTTP)
  - beautifulsoup4 (pour parser le HTML)
  - pandas (pour creer le fichier CSV)

## Installation

1. Cloner le repository
2. Creer l'environnement virtuel :
```bash
python -m venv venv
```

3. Activer l'environnement virtuel :
- Windows : `venv\Scripts\activate`
- Linux/Mac : `source venv/bin/activate`

4. Installer les dependances :
```bash
pip install -r requirements.txt
```

## Utilisation

Lancer le script :
```bash
python scraper.py
```

Le script va :
1. Tester la connexion au site Free-Work (status 200)
2. Parcourir les pages d'offres configurees (par defaut 1 page)
3. Pour chaque offre, acceder a la page de detail
4. Extraire les informations : titre, entreprise, salaire, description
5. Sauvegarder les donnees dans `offres_emploi.csv`

## Configuration

Dans le fichier `scraper.py`, vous pouvez modifier :
- `nombre_pages` : nombre de pages a scraper (ligne 32, par defaut 1)
- `DELAY` : delai en secondes entre chaque page (ligne 17, par defaut 3s)
- `base_url` : URL de base pour le scraping (ligne 16)

## Structure des donnees extraites

Le fichier CSV contient 4 colonnes :
- **titre** : Titre du poste (ex: "Chef de Projet Agile SAFe (H/F)")
- **entreprise** : Nom de l'entreprise (ex: "Groupe Aptenia", "Link Consulting")
- **salaire** : Fourchette de salaire TJM ou annuel (ex: "500-600 EUR/j", "45k-49k EUR/an")
- **description** : Description du poste (premiers 300 caracteres)

## Analyse technique (Inspection DOM)

Identification des elements HTML par inspection du code source (F12) :

**Sur la page de liste :**
- Liens vers les offres : `<a href="/fr/tech-it/jobs/...">` avec attribut href contenant "/jobs/"

**Sur la page de detail de chaque offre :**
- **Titre** : `<h2 class="font-semibold text-xl mb-4">...</h2>`
- **Entreprise** : `<div class="font-bold">...</div>`
- **Salaire** : `<span class="text-sm truncate w-full">500-600 EUR/j</span>` (contient "EUR" ou "k")
- **Description** : `<div class="fw-text-highlight line-clamp-4 break-anywhere">...</div>`

## Approche de developpement (methodologie iterative)

Le projet suit la methodologie du prof en 4 etapes :

1. **Etape 1** : Test de connexion (verification status 200)
2. **Etape 2** : Extraction sur une seule page (affichage des titres)
3. **Etape 3** : Gestion de la pagination (boucle sur plusieurs pages)
4. **Etape 4** : Robustesse (try/except pour gerer les erreurs)

Puis stockage en CSV avec Pandas.

## Ethique et bonnes pratiques

- User-Agent personnalise pour se presenter poliment au serveur
- Pause de 3 secondes entre chaque page (DELAY)
- Pause de 1 seconde entre chaque offre
- Gestion des erreurs 429 (Too Many Requests) sans planter le script
- Respect des limitations du site

## Limitations connues

- Le site Free-Work peut limiter le nombre de requetes (erreur 429 apres ~30 offres)
- Certaines donnees peuvent etre manquantes (affichees comme "N/C")
- Certains liens pointent vers des pages de competences plutot que de vraies offres
- La pagination peut retourner des resultats similaires

## Resultats obtenus

- **90 offres extraites** (objectif : 50-100)
- **4 colonnes** : Titre, Entreprise, Salaire, Description
- Donnees coherentes avec de vraies entreprises
- Gestion robuste des erreurs


Projet realise dans le cadre de l'atelier Analyse de donnees
