import pickle
import json
from datetime import datetime  # Import pour ajouter un horodatage

# Charge les données de recommandations au démarrage de la fonction
with open("top_n_final.txt", "rb") as fp:
    top_n = pickle.load(fp)

def function_ocr(request):
    # Vérifie que la méthode de la requête est GET
    if request.method == 'GET':
        # Récupérer l'ID utilisateur de l'URL
        user_id = request.args.get('user_id') 
        
        if user_id is not None:
            user_id = int(user_id)  # Convertir l'ID utilisateur en entier
            
            # Vérifie si l'utilisateur existe dans les recommandations
            if user_id in top_n:
                recommendations = [
                    {"category_id": category_id, "estimated_rating": estimated_rating}
                    for category_id, estimated_rating in top_n[user_id]
                ]
                # Ajout d'un horodatage dans la réponse
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return json.dumps({"user_id": user_id, 
                                   "recommendations": recommendations, 
                                   "timestamp": timestamp}), 200, {'Content-Type': 'application/json'}
            else:
                return json.dumps({"error": "User ID not found"}), 404, {'Content-Type': 'application/json'}
        else:
            return json.dumps({"error": "User ID parameter is required"}), 400, {'Content-Type': 'application/json'}
    else:
        return json.dumps({"error": "Method not allowed"}), 405, {'Content-Type': 'application/json'}
