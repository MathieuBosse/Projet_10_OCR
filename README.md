# Système de Recommandation basé sur Google Cloud et Streamlit

Ce dépôt contient le code et les instructions pour un système de recommandation construit avec **Google Cloud Platform** (GCP) et une interface utilisateur développée avec **Streamlit**. Ce projet met en œuvre deux architectures :

1. Une architecture basée sur des recommandations pré-calculées et exposées via une **Google Cloud Function**.
2. Une architecture automatisée pour mettre à jour les recommandations en réponse à des changements dans les données utilisateur, via un pipeline déclenché par des événements dans **Google Cloud Storage**.

---

## Table des Matières

- [Aperçu du Projet](#aperçu-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Architecture](#architecture)
  - [Première Architecture](#première-architecture)
  - [Deuxième Architecture](#deuxième-architecture)
- [Dépôt des Fichiers](#dépôt-des-fichiers)
- [Licence](#licence)

---

## Aperçu du Projet

Ce système de recommandation permet de fournir des suggestions personnalisées à des utilisateurs en fonction de leurs interactions passées.  
Il est conçu pour être scalable, performant et facile à maintenir grâce à l’utilisation des services GCP.

L'interface utilisateur est simple et intuitive, développée avec Streamlit pour permettre aux utilisateurs d’interagir avec le système. Deux architectures sont proposées pour répondre à des besoins variés :

1. **Recommandations pré-calculées** : Simplicité et rapidité d'exécution en temps réel.
2. **Pipeline automatisé** : Recalcul des recommandations à chaque mise à jour des données.

---

## Fonctionnalités

### Première Architecture
- Interface utilisateur avec **Streamlit**.
- Recommandations personnalisées via une **API Google Cloud Function**.
- Gestion sécurisée des données avec **Cloud IAM**.
- Rapidité d'exécution grâce aux recommandations pré-calculées.

### Deuxième Architecture
- Automatisation des mises à jour via des **déclencheurs d'événements** dans **Google Cloud Storage**.
- Entraînement ou mise à jour du modèle de recommandation.
- Génération des recommandations et stockage dans le bucket GCP.

---

## Prérequis

- **Google Cloud Platform** : Projet configuré avec Cloud Functions, Cloud Storage et IAM.
- **Python 3.10+** : Pour exécuter l'application Streamlit et les scripts backend.
- **Bibliothèques Python** : Voir `requirements.txt`.
- **CLI Google Cloud** : Pour déployer et gérer les fonctions sur GCP.

---

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/MathieuBosse/Projet_10_OCR.git
   cd Projet_10_OCR
   ```

2. Configurez un environnement virtuel :
   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows : env\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Configurez votre environnement Google Cloud :

   - Authentifiez-vous :
     ```bash
     gcloud auth login
     ```

   - Sélectionnez le projet :
     ```bash
     gcloud config set project [PROJECT_ID]
     ```
---

## Utilisation

### Exécution locale de l'application Streamlit

1. Lancer l'application Streamlit :
   ```bash
   streamlit run app.py
   ```
   Ouvrez votre navigateur à l'URL affichée (généralement http://localhost:8501).

2. Saisissez un ID utilisateur dans le champ prévu et cliquez sur "Obtenir des recommandations".

### Déploiement de la Google Cloud Function

Placez les fichiers nécessaires dans un répertoire (par exemple : `main.py`, `requirements.txt`, données).

Déployez la fonction :

```bash
gcloud functions deploy [NOM_FONCTION] \
    --runtime python310 \
    --trigger-http \
    --entry-point [NOM_POINT_ENTREE]
```

Utilisez l'URL générée pour interagir avec l'API.

### Architecture

#### Première Architecture
Les recommandations sont pré-calculées et stockées dans Google Cloud Storage.  
Une Google Cloud Function récupère ces données à la demande et les renvoie à l'application Streamlit via HTTP.  
Voir la description complète.

#### Deuxième Architecture
Les modifications dans le bucket GCP déclenchent un pipeline qui entraîne ou met à jour le modèle de recommandation.  
Les résultats sont sauvegardés dans le bucket pour un accès futur.  
Voir la description complète.

### Dépôt des Fichiers

- `app.py` : Script principal de l'application Streamlit.
- `main.py` : Code de la Google Cloud Function.
- `requirements.txt` : Dépendances Python nécessaires.
- `data/` : Exemple de données utilisateur et articles (non inclus pour confidentialité).
- `README.md` : Documentation du projet (ce fichier).

### Licence

Ce projet est distribué sous la licence MIT. Veuillez consulter le fichier `LICENSE` pour plus d'informations.

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue ou à me contacter.
