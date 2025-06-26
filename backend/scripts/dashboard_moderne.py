import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output, callback_context
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os
import sys

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Vérifier si les données existent, sinon exécuter l'ETL
if not os.path.exists('data/covid_processed.csv') or not os.path.exists('data/mpox_processed.csv'):
    print("Les données transformées n'existent pas. Exécution du script ETL...")
    try:
        import etl_script
        etl_script.main()
    except Exception as e:
        print(f"Erreur lors de l'exécution de l'ETL: {e}")

# Chargement des données
def load_data():
    """Charger et préparer les données"""
    try:
        # Données COVID-19
        covid_df = pd.read_csv('data/covid_processed.csv')
        covid_df['date'] = pd.to_datetime(covid_df['date'])
        
        # Données Mpox
        mpox_df = pd.read_csv('data/mpox_processed.csv')
        if 'date' in mpox_df.columns:
            mpox_df['date'] = pd.to_datetime(mpox_df['date'], errors='coerce')
        elif 'Date_confirmation' in mpox_df.columns:
            mpox_df['date'] = pd.to_datetime(mpox_df['Date_confirmation'], errors='coerce')
        
        return covid_df, mpox_df
    except Exception as e:
        print(f"Erreur lors du chargement des données: {e}")
        return None, None

covid_df, mpox_df = load_data()

# Initialisation de l'application Dash
app = dash.Dash(__name__, 
                title="Dashboard COVID-19 & Mpox",
                external_stylesheets=[
                    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
                ])

# Configuration du thème
colors = {
    'background': '#f8f9fa',
    'text': '#2c3e50',
    'primary': '#3498db',
    'secondary': '#e74c3c',
    'success': '#27ae60',
    'warning': '#f39c12'
}

# Layout du dashboard
app.layout = html.Div([
    # Header
    html.Div([
        html.H1([
            html.I(className="fas fa-chart-line", style={'marginRight': '10px'}),
            "Dashboard COVID-19 & Mpox"
        ], style={'textAlign': 'center', 'color': colors['text'], 'marginBottom': '30px'})
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    
    # Filtres globaux
    html.Div([
        html.H3("🎚️ Filtres", style={'color': colors['text'], 'marginBottom': '15px'}),
        
        html.Div([
            # Filtre pays
            html.Div([
                html.Label("📍 Pays:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='country-filter',
                    options=[{'label': country, 'value': country} 
                            for country in sorted(covid_df['location'].unique()) if pd.notna(country)] if covid_df is not None else [],
                    value=['France', 'United States', 'Germany', 'China', 'Brazil'],
                    multi=True,
                    placeholder="Sélectionner des pays...",
                    style={'marginBottom': '15px'}
                )
            ], style={'flex': '1', 'marginRight': '20px'}),
            
            # Filtre période
            html.Div([
                html.Label("📅 Période:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.DatePickerRange(
                    id='date-filter',
                    min_date_allowed=covid_df['date'].min() if covid_df is not None else datetime.now() - timedelta(days=365),
                    max_date_allowed=covid_df['date'].max() if covid_df is not None else datetime.now(),
                    start_date=covid_df['date'].min() if covid_df is not None else datetime.now() - timedelta(days=365),
                    end_date=covid_df['date'].max() if covid_df is not None else datetime.now(),
                    style={'marginBottom': '15px'}
                )
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'marginBottom': '20px'})
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginBottom': '20px'}),
    
    # Graphiques
    html.Div([
        # Première ligne : Évolution COVID-19 et Vaccinés par pays
        html.Div([
            # Évolution des cas COVID-19
            html.Div([
                html.H3("📈 Évolution des cas COVID-19", style={'color': colors['text'], 'marginBottom': '15px'}),
                dcc.Graph(id='covid-evolution-chart', style={'height': '400px'})
            ], style={'flex': '1', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginRight': '10px'}),
            
            # Nombre de vaccinés par pays
            html.Div([
                html.H3("💉 Nombre de vaccinés par pays", style={'color': colors['text'], 'marginBottom': '15px'}),
                dcc.Graph(id='vaccination-chart', style={'height': '400px'})
            ], style={'flex': '1', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginLeft': '10px'})
        ], style={'display': 'flex', 'marginBottom': '20px'}),
        
        # Deuxième ligne : Cas Mpox et Comparaison
        html.Div([
            # Cas totaux Mpox par pays
            html.Div([
                html.H3("🦠 Cas totaux Mpox par pays", style={'color': colors['text'], 'marginBottom': '15px'}),
                dcc.Graph(id='mpox-chart', style={'height': '400px'})
            ], style={'flex': '1', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginRight': '10px'}),
            
            # Comparaison COVID vs Mpox
            html.Div([
                html.H3("⚖️ Comparaison COVID vs Mpox", style={'color': colors['text'], 'marginBottom': '15px'}),
                dcc.Graph(id='comparison-chart', style={'height': '400px'})
            ], style={'flex': '1', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginLeft': '10px'})
        ], style={'display': 'flex'})
    ]),
    
    # Footer avec statistiques
    html.Div([
        html.H3("📊 Statistiques globales", style={'color': colors['text'], 'marginBottom': '15px'}),
        html.Div(id='global-stats', style={'display': 'flex', 'justifyContent': 'space-around'})
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginTop': '20px'})
], style={'backgroundColor': colors['background'], 'padding': '20px', 'minHeight': '100vh'})

# Callbacks
@app.callback(
    [Output('covid-evolution-chart', 'figure'),
     Output('vaccination-chart', 'figure'),
     Output('mpox-chart', 'figure'),
     Output('comparison-chart', 'figure'),
     Output('global-stats', 'children')],
    [Input('country-filter', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')]
)
def update_charts(countries, start_date, end_date):
    if not countries or covid_df is None:
        return {}, {}, {}, {}, []
    
    # Conversion des dates
    start_date = pd.to_datetime(start_date) if start_date else covid_df['date'].min()
    end_date = pd.to_datetime(end_date) if end_date else covid_df['date'].max()
    
    # Filtrage des données COVID
    filtered_covid = covid_df[
        (covid_df['location'].isin(countries)) & 
        (covid_df['date'] >= start_date) & 
        (covid_df['date'] <= end_date)
    ]
    
    # 1. Évolution des cas COVID-19 (courbe)
    covid_evolution = px.line(
        filtered_covid,
        x='date',
        y='total_cases',
        color='location',
        title="Évolution des cas COVID-19",
        labels={'total_cases': 'Cas totaux', 'date': 'Date', 'location': 'Pays'}
    )
    covid_evolution.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': colors['text']},
        hovermode='x unified'
    )
    
    # 2. Nombre de vaccinés par pays (barres horizontales)
    latest_covid = filtered_covid.sort_values('date').groupby('location').last().reset_index()
    vaccination_data = latest_covid[latest_covid['people_vaccinated'].notna() & (latest_covid['people_vaccinated'] > 0)]
    
    vaccination_chart = px.bar(
        vaccination_data,
        x='people_vaccinated',
        y='location',
        orientation='h',
        title="Nombre de vaccinés par pays",
        labels={'people_vaccinated': 'Nombre de vaccinés', 'location': 'Pays'},
        color='people_vaccinated',
        color_continuous_scale='Blues'
    )
    vaccination_chart.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': colors['text']},
        yaxis={'categoryorder': 'total ascending'}
    )
    
    # 3. Cas totaux Mpox par pays (barres verticales)
    if mpox_df is not None and not mpox_df.empty:
        # Filtrer les pays sélectionnés dans les données mpox
        available_countries = [c for c in countries if c in mpox_df['location'].unique()]
        if available_countries:
            filtered_mpox = mpox_df[mpox_df['location'].isin(available_countries)]
            mpox_by_country = filtered_mpox.groupby('location')['total_cases'].sum().reset_index()
            
            mpox_chart = px.bar(
                mpox_by_country,
                x='location',
                y='total_cases',
                title="Cas totaux Mpox par pays",
                labels={'total_cases': 'Cas totaux', 'location': 'Pays'},
                color='total_cases',
                color_continuous_scale='Reds'
            )
            mpox_chart.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': colors['text']},
                xaxis={'categoryorder': 'total descending'}
            )
        else:
            mpox_chart = px.bar(
                title="Aucune donnée Mpox disponible pour les pays sélectionnés"
            )
    else:
        mpox_chart = px.bar(
            title="Données Mpox non disponibles"
        )
    
    # 4. Comparaison COVID vs Mpox (graphique combiné)
    if mpox_df is not None and not mpox_df.empty:
        # Préparer les données pour la comparaison
        covid_latest = latest_covid[['location', 'total_cases']].rename(columns={'total_cases': 'covid_cases'})
        
        available_countries = [c for c in countries if c in mpox_df['location'].unique()]
        if available_countries:
            mpox_latest = mpox_df[mpox_df['location'].isin(available_countries)].groupby('location')['total_cases'].sum().reset_index()
            mpox_latest = mpox_latest.rename(columns={'total_cases': 'mpox_cases'})
            
            # Fusionner les données
            comparison_data = covid_latest.merge(mpox_latest, on='location', how='inner')
            
            # Créer un graphique combiné
            comparison_chart = go.Figure()
            
            comparison_chart.add_trace(go.Bar(
                x=comparison_data['location'],
                y=comparison_data['covid_cases'],
                name='COVID-19',
                marker_color=colors['primary']
            ))
            
            comparison_chart.add_trace(go.Bar(
                x=comparison_data['location'],
                y=comparison_data['mpox_cases'],
                name='Mpox',
                marker_color=colors['secondary']
            ))
            
            comparison_chart.update_layout(
                title="Comparaison COVID-19 vs Mpox par pays",
                barmode='group',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': colors['text']},
                xaxis={'title': 'Pays'},
                yaxis={'title': 'Nombre de cas'}
            )
        else:
            comparison_chart = px.bar(
                title="Aucune donnée de comparaison disponible"
            )
    else:
        comparison_chart = px.bar(
            title="Données de comparaison non disponibles"
        )
    
    # 5. Statistiques globales
    stats = []
    if not filtered_covid.empty:
        total_cases = filtered_covid['total_cases'].max()
        total_deaths = filtered_covid['total_deaths'].max()
        total_vaccinated = filtered_covid['people_vaccinated'].max()
        
        stats = [
            html.Div([
                html.H4(f"{total_cases:,.0f}", style={'color': colors['primary'], 'margin': '0'}),
                html.P("Cas COVID-19", style={'margin': '0', 'fontSize': '14px'})
            ], style={'textAlign': 'center', 'padding': '10px'}),
            html.Div([
                html.H4(f"{total_deaths:,.0f}", style={'color': colors['secondary'], 'margin': '0'}),
                html.P("Décès COVID-19", style={'margin': '0', 'fontSize': '14px'})
            ], style={'textAlign': 'center', 'padding': '10px'}),
            html.Div([
                html.H4(f"{total_vaccinated:,.0f}", style={'color': colors['success'], 'margin': '0'}),
                html.P("Vaccinés", style={'margin': '0', 'fontSize': '14px'})
            ], style={'textAlign': 'center', 'padding': '10px'})
        ]
    
    return covid_evolution, vaccination_chart, mpox_chart, comparison_chart, stats

if __name__ == '__main__':
    print("Démarrage du dashboard...")
    print("Accédez au dashboard à l'adresse: http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050) 