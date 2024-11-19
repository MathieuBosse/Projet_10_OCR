import pandas as pd
import pickle
import numpy as np
from surprise import Dataset, Reader, SVD
from collections import defaultdict
from google.cloud import storage
import os
import json

# Initialiser le client Google Cloud Storage
storage_client = storage.Client()

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Télécharge un blob depuis le bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Télécharge un fichier vers le bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

def get_top_n(predictions, n=5):
    """Retourne les top-N recommandations pour chaque utilisateur à partir d'un ensemble de prédictions."""
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))
    
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    
    return top_n

def process_files(event, context):
    # Configuration des noms de bucket et des fichiers
    bucket_name = 'my-data-bucket-architecture-n2'  # Remplacez par le nom de votre bucket
    clicks_file = 'clicks.csv'
    articles_metadata_file = 'articles_metadata.csv'
    model_file = 'svd_model.pkl'  # Nom du fichier pour le modèle

    # Téléchargement des fichiers depuis Google Cloud Storage
    try:
        download_blob(bucket_name, clicks_file, '/tmp/clicks.csv')
        print(f"Téléchargement réussi : {clicks_file} a été téléchargé dans /tmp/clicks.csv.")
    except Exception as e:
        print(f"Erreur lors du téléchargement de {clicks_file} : {e}")

    try:
        download_blob(bucket_name, articles_metadata_file, '/tmp/articles_metadata.csv')
        print(f"Téléchargement réussi : {articles_metadata_file} a été téléchargé dans /tmp/articles_metadata.csv.")
    except Exception as e:
        print(f"Erreur lors du téléchargement de {articles_metadata_file} : {e}")

    # Lire les fichiers CSV
    clicks = pd.read_csv('/tmp/clicks.csv')
    articles_metadata = pd.read_csv('/tmp/articles_metadata.csv')

    # Fusion des données
    dataframe = clicks.merge(articles_metadata, left_on='click_article_id', right_on='article_id')
    dataframe = dataframe[['user_id', 'article_id', 'category_id']]

    # Création de la matrice utilisateur/catégorie
    series = dataframe.groupby(['user_id', 'category_id']).size()
    user_rating_matrix = series.to_frame().reset_index()
    user_rating_matrix.rename(columns={0: 'rate'}, inplace=True)

    # Nettoyage des valeurs où la note dépasse 10
    user_rating_matrix_cleaned = user_rating_matrix[user_rating_matrix['rate'] <= 10]

    # Construire le dataset Surprise
    reader = Reader(rating_scale=(1, 10))
    _x = user_rating_matrix_cleaned.loc[user_rating_matrix_cleaned.rate > 1]
    data = Dataset.load_from_df(_x[['user_id', 'category_id', 'rate']], reader)

    print('We have selected', len(_x), 'interactions.')

    # Obtenir le trainset complet
    full_trainset = data.build_full_trainset()

    # Vérifier si le modèle est déjà stocké
    model_path = '/tmp/svd_model.pkl'
    try:
        download_blob(bucket_name, model_file, model_path)
        with open(model_path, 'rb') as f:
            algo = pickle.load(f)
        print("Modèle chargé avec succès.")
    except Exception as e:
        print("Le modèle n'a pas été trouvé, entraînement d'un nouveau modèle.")
        # Charger ou définir un modèle d'algorithme (exemple : SVD)
        algo = SVD()  # Utiliser SVD ou tout autre algorithme que vous préférez
        algo.fit(full_trainset)

        # Sauvegarder le modèle dans Google Cloud Storage
        with open(model_path, 'wb') as f:
            pickle.dump(algo, f)
        upload_blob(bucket_name, model_path, model_file)

    # Construire un testset correspondant avec toutes les interactions possibles
    full_testset = full_trainset.build_testset()

    # Faire des prédictions
    predictions_data = algo.test(full_testset)

    # Obtenir le top-N des recommandations
    top_n = get_top_n(predictions_data, n=5)

    # Sauvegarder les résultats dans un fichier
    with open("/tmp/top_n_final.txt", "w") as fp:
        json.dump(top_n, fp)  # Utilisez json.dump pour écrire le contenu en format texte

    try:
        upload_blob(bucket_name, '/tmp/top_n_final.txt', 'top_n_final.txt')
        print("Fichier de résultats uploadé dans le bucket avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'upload du fichier de résultats : {e}")