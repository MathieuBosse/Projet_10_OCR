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

#### Activer les API nécessaires 

```bash
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

#### Déploiement pour la Première Architecture  
Les recommandations sont pré-calculées et stockées dans Google Cloud Storage.  
Une Google Cloud Function récupère ces données à la demande et les renvoie à l'application Streamlit via HTTP.  
Voir la description complète.

Placez les fichiers nécessaires dans un répertoire (par exemple : `main.py`, `requirements.txt`, données).

Déployez la fonction :

```bash
gcloud functions deploy function-ocr \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated \
    --source . \
    --entry-point function_ocr
```

Utilisez l'URL générée pour interagir avec l'API.

**Remarques :**
- La fonction sera accessible via une URL HTTP générée automatiquement après le déploiement.
- Le script `function_ocr` doit être adapté pour récupérer les données pré-calculées stockées dans Google Cloud Storage.


#### Déploiement pour la Deuxième Architecture  

Dans cette architecture, la fonction est déclenchée par un événement dans un bucket Google Cloud Storage.

Assurez-vous que le bucket de stockage et la fonction sont situés dans la même région.

Utilisez la commande suivante :

```bash
gcloud functions deploy process-files \
    --runtime python310 \
    --trigger-resource [BUCKET_NAME] \
    --trigger-event google.storage.object.finalize \
    --entry-point process_files \
    --memory 512MB \
    --region europe-west9 \
    --allow-unauthenticated
```
**Remarques :**
- Remplacez `[BUCKET_NAME]` par le nom de votre bucket Google Cloud Storage.
- La région `europe-west9` peut être ajustée en fonction de vos besoins.
- Le script `process_files` doit être conçu pour entraîner ou mettre à jour le modèle en fonction des nouvelles données détectées dans le bucket.

#### Conclusion
Les deux architectures de déploiement permettent de gérer efficacement les recommandations en fonction de vos besoins :

1. **Première Architecture** : Utilise une fonction HTTP pour fournir des recommandations pré-calculées à la demande, idéale pour des cas d'usage simples où la rapidité et la simplicité sont prioritaires.
2. **Deuxième Architecture** : Permet une mise à jour automatique des recommandations via un pipeline déclenché par des événements dans un bucket Google Cloud Storage, parfait pour des applications dynamiques nécessitant des mises à jour fréquentes du modèle.

Dans les deux cas, assurez-vous que votre configuration Google Cloud, y compris les services et permissions, soit correctement définie pour permettre une communication fluide entre vos composants.

### Dépôt des Fichiers

- `app.py` : Script principal de l'application Streamlit.
- `main.py` : Code de la Google Cloud Function.
- `requirements.txt` : Dépendances Python nécessaires.
- `data/` : Exemple de données utilisateur et articles (non inclus pour confidentialité).
- `README.md` : Documentation du projet (ce fichier).

### Licence

Ce projet est distribué sous la licence MIT. Veuillez consulter le fichier `LICENSE` pour plus d'informations.

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue ou à me contacter.
