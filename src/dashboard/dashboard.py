import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import requests

# URL de l'API locale
api_url = "http://127.0.0.1:5000/predict"

# Charger les données localement depuis un fichier CSV
df = pd.read_csv('merged_data_grouped.csv')

# Initialiser l'application Dash avec le thème Bootstrap
app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])
server = app.server  # Ajouter cette ligne pour que Gunicorn puisse trouver l'application Flask interne

app.layout = html.Div(
    className="container mt-4",
    children=[
        html.H1("Dashboard Interactif", className="text-center mb-4"),
        
        html.Div(
            className="row mb-4",
            children=[
                html.Div(
                    className="col-md-6",
                    children=[
                        dcc.Dropdown(
                            id='client-dropdown',
                            options=[{'label': str(client_id), 'value': client_id} for client_id in df['SK_ID_CURR'].unique()],
                            placeholder='Sélectionnez un client',
                            className="form-control"
                        )
                    ]
                ),
                html.Div(id='client-info', className="col-md-6 text-center")
            ]
        ),
        
        dcc.Graph(id='comparison-graph', className="mt-4")
    ]
)

@app.callback(
    [Output('client-info', 'children'), Output('comparison-graph', 'figure')],
    [Input('client-dropdown', 'value')]
)
def update_dashboard(client_id):
    if client_id is None:
        return 'Veuillez sélectionner un client.', {}
    
    # Interroger l'API locale pour obtenir la prédiction
    response = requests.post(api_url, json={"client_id": client_id})
    
    # Vérifier la réponse de l'API
    if response.status_code != 200:
        return 'Erreur lors de la récupération des données.', {}

    result = response.json()

    # Vérifier les erreurs
    if 'error' in result:
        return f"Erreur: {result['error']}", {}

    # Score et interprétation de l'API
    score = result['prediction']
    proba = result['probability']
    interpretation = "Crédit approuvé" if score == 0 else "Crédit refusé"
    
    client_info = html.Div(
        [
            html.H4(f"Score du client: {score} ({interpretation})", className="mt-3"),
            html.P(f"Probabilité: {proba:.2f}", className="lead")
        ],
        className="alert alert-info"
    )

    # Comparaison du client avec l'ensemble des clients
    fig = px.histogram(df, x='AMT_INCOME_TOTAL', color='TARGET', title='Comparaison des revenus totaux')
    fig.add_vline(x=df[df['SK_ID_CURR'] == client_id]['AMT_INCOME_TOTAL'].values[0], line_dash="dash", line_color="red")

    # Amélioration des visuels du graphique
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        title_font=dict(size=16, color='blue')
    )

    return client_info, fig

if __name__ == '__main__':
    app.run_server(debug=False)
