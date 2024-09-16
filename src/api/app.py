import pandas as pd
from flask import Flask, request, jsonify
from joblib import load

# Charger le modèle et le pipeline
model = load('random_forest_model_optimised.joblib')
pipeline = load('pipeline.joblib')

# Lire le fichier CSV localement lors de l'initialisation de l'application
data = pd.read_csv('merged_data_grouped.csv')

# Initialisation de l'application Flask
app = Flask(__name__)

def get_client_data(client_id):
    # Filtrer les informations du client par son identifiant à partir des données préchargées
    df_client = data[data['SK_ID_CURR'] == client_id]
    if not df_client.empty:
        return df_client
    return None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Vérifier si 'client_id' est dans la requête JSON
        if 'client_id' not in request.json:
            return jsonify({'error': 'client_id is missing from request'}), 400

        # Récupérer l'identifiant client
        client_id = request.json['client_id']
        
        # Récupérer les données du client
        df_client = get_client_data(client_id)
        
        # Vérifier si le client existe
        if df_client is None or df_client.empty:
            return jsonify({'error': 'Client not found'}), 404

        # Préparer les données du client pour la prédiction
        X_client = df_client.drop('TARGET', axis=1)
        
        # Appliquer le pipeline de transformation
        X_client_transformed = pipeline.transform(X_client)
        
        # Faire une prédiction
        prediction = model.predict(X_client_transformed)[0]
        prediction_proba = model.predict_proba(X_client_transformed)[0][1]

        # Retourner le résultat sous forme de JSON
        return jsonify({'prediction': int(prediction), 'probability': float(prediction_proba)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
