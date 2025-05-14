import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Vérifier si les données existent, sinon exécuter l'ETL
if not os.path.exists('data/covid_processed.csv') or not os.path.exists('data/mpox_processed.csv'):
    print("Les données transformées n'existent pas. Exécution du script ETL...")
    import scripts.etl_script as etl_script
    etl_script.main()

# Chargement des données
covid_df = pd.read_csv('data/covid_processed.csv')
covid_df['date'] = pd.to_datetime(covid_df['date'])

try:
    mpox_df = pd.read_csv('data/mpox_processed.csv')
    # Vérifier la structure des données mpox et adapter si nécessaire
    if 'Date_confirmation' in mpox_df.columns:
        mpox_df['Date_confirmation'] = pd.to_datetime(mpox_df['Date_confirmation'], errors='coerce')
        print("Colonnes disponibles dans mpox_df:", mpox_df.columns.tolist())
    else:
        # Rechercher une colonne de date
        date_cols = [col for col in mpox_df.columns if any(x in col.lower() for x in ['date', 'time'])]
        if date_cols:
            mpox_df.rename(columns={date_cols[0]: 'Date_confirmation'}, inplace=True)
            mpox_df['Date_confirmation'] = pd.to_datetime(mpox_df['Date_confirmation'], errors='coerce')
except Exception as e:
    print(f"Erreur lors du chargement des données mpox: {e}")
    mpox_df = None

# Initialisation de l'application Dash
app = dash.Dash(__name__, title="Dashboard COVID-19 et Mpox")

# Layout du dashboard
app.layout = html.Div([
    html.H1("Dashboard COVID-19 et Mpox", style={'textAlign': 'center'}),
    
    # Sélection des onglets
    dcc.Tabs([
        # Onglet COVID-19
        dcc.Tab(label="COVID-19", children=[
            html.Div([
                html.H3("Analyse COVID-19", style={'textAlign': 'center'}),
                
                # Filtres
                html.Div([
                    html.Label("Sélectionner des pays:"),
                    dcc.Dropdown(
                        id='covid-country-dropdown',
                        options=[{'label': country, 'value': country} 
                                for country in sorted(covid_df['location'].unique())],
                        value=['France', 'United States', 'Germany', 'China', 'Brazil'],
                        multi=True
                    ),
                    
                    html.Label("Sélectionner une métrique:"),
                    dcc.RadioItems(
                        id='covid-metric-radio',
                        options=[
                            {'label': 'Cas totaux', 'value': 'total_cases'},
                            {'label': 'Nouveaux cas', 'value': 'new_cases'},
                            {'label': 'Décès totaux', 'value': 'total_deaths'},
                            {'label': 'Nouveaux décès', 'value': 'new_deaths'},
                            {'label': 'Hospitalisations', 'value': 'hosp_patients'}
                        ],
                        value='total_cases',
                        labelStyle={'display': 'inline-block', 'marginRight': '10px'}
                    ),
                    
                    html.Label("Plage de dates:"),
                    dcc.DatePickerRange(
                        id='covid-date-picker',
                        min_date_allowed=covid_df['date'].min(),
                        max_date_allowed=covid_df['date'].max(),
                        start_date=covid_df['date'].min(),
                        end_date=covid_df['date'].max()
                    )
                ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
                
                # Graphiques
                html.Div([
                    dcc.Graph(id='covid-line-chart'),
                    dcc.Graph(id='covid-bar-chart')
                ]),
                
                # Statistiques
                html.Div(id='covid-stats', style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px', 'marginTop': '20px'})
            ])
        ]),
        
        # Onglet Mpox
        dcc.Tab(label="Mpox", children=[
            html.Div([
                html.H3("Analyse Mpox", style={'textAlign': 'center'}),
                
                # Message si les données ne sont pas disponibles
                html.Div(id='mpox-data-status'),
                
                # Contenu conditionnel basé sur la disponibilité des données
                html.Div(id='mpox-content')
            ])
        ]),
        
        # Onglet Comparatif
        dcc.Tab(label="Comparaison", children=[
            html.Div([
                html.H3("Comparaison COVID-19 vs Mpox", style={'textAlign': 'center'}),
                
                html.Div([
                    html.Label("Sélectionner des pays:"),
                    dcc.Dropdown(
                        id='compare-country-dropdown',
                        options=[{'label': country, 'value': country} 
                                for country in sorted(covid_df['location'].unique())],
                        value=['France', 'United States', 'Germany'],
                        multi=True
                    )
                ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
                
                # Graphique comparatif
                dcc.Graph(id='comparison-chart')
            ])
        ])
    ])
])

# Callbacks pour COVID-19
@app.callback(
    [Output('covid-line-chart', 'figure'),
     Output('covid-bar-chart', 'figure'),
     Output('covid-stats', 'children')],
    [Input('covid-country-dropdown', 'value'),
     Input('covid-metric-radio', 'value'),
     Input('covid-date-picker', 'start_date'),
     Input('covid-date-picker', 'end_date')]
)
def update_covid_graphs(countries, metric, start_date, end_date):
    # Filtrer les données
    filtered_df = covid_df[
        (covid_df['location'].isin(countries)) & 
        (covid_df['date'] >= start_date) & 
        (covid_df['date'] <= end_date)
    ]
    
    # Graphique d'évolution temporelle
    line_fig = px.line(
        filtered_df, 
        x='date', 
        y=metric,
        color='location',
        title=f"Évolution de {metric.replace('_', ' ')} par pays"
    )
    
    # Graphique à barres des dernières valeurs
    latest_data = filtered_df.sort_values('date').groupby('location').last().reset_index()
    bar_fig = px.bar(
        latest_data, 
        x='location', 
        y=metric,
        title=f"Dernières valeurs de {metric.replace('_', ' ')} par pays",
        color='location'
    )
    
    # Statistiques
    stats = []
    
    for country in countries:
        country_data = filtered_df[filtered_df['location'] == country]
        if not country_data.empty:
            latest_value = country_data.sort_values('date').iloc[-1][metric]
            max_value = country_data[metric].max()
            stats.append(html.Div([
                html.H4(country),
                html.P(f"Dernière valeur de {metric.replace('_', ' ')}: {latest_value:,.0f}"),
                html.P(f"Valeur maximale: {max_value:,.0f}")
            ]))
    
    return line_fig, bar_fig, stats

# Callback pour vérifier la disponibilité des données Mpox
@app.callback(
    [Output('mpox-data-status', 'children'),
     Output('mpox-content', 'children')],
    [Input('mpox-data-status', 'id')]  # Dummy input pour déclencher le callback au chargement
)
def check_mpox_data(_):
    if mpox_df is None or mpox_df.empty:
        return (
            html.Div([
                html.H4("Données Mpox non disponibles", style={'color': 'red'}),
                html.P("Les données mpox n'ont pas pu être chargées. Veuillez exécuter le script ETL.")
            ]),
            None
        )
    
    # Identifier les colonnes clés dans le dataframe mpox
    country_col = next((col for col in mpox_df.columns if col.lower() in ['country', 'location'] or 'country' in col.lower() or 'nation' in col.lower()), None)
    date_col = next((col for col in mpox_df.columns if col.lower() in ['date_confirmation', 'date'] or 'date' in col.lower()), None)
    case_col = next((col for col in mpox_df.columns if col.lower() in ['cases', 'total_cases'] or 'case' in col.lower()), None)
    
    print(f"Colonnes détectées - Pays: {country_col}, Date: {date_col}, Cas: {case_col}")
    
    if country_col is None:
        return (
            html.Div([
                html.H4("Structure des données Mpox non reconnue", style={'color': 'orange'}),
                html.P("Le format des données mpox est différent de celui attendu.")
            ]),
            html.Div([
                html.P("Colonnes disponibles:"),
                html.Code(", ".join(mpox_df.columns.tolist())),
                dcc.Graph(
                    figure=px.bar(
                        mpox_df.iloc[:, 0].value_counts().reset_index(),
                        x='index',
                        y='count',
                        title="Distribution par première colonne"
                    )
                )
            ])
        )
    
    # Préparation des filtres pour les métriques
    metric_filter = None
    if 'total_cases' in mpox_df.columns and 'new_cases' in mpox_df.columns:
        metric_filter = html.Div([
            html.Label("Sélectionner une métrique:"),
            dcc.RadioItems(
                id='mpox-metric-radio',
                options=[
                    {'label': 'Cas totaux', 'value': 'total_cases'},
                    {'label': 'Nouveaux cas', 'value': 'new_cases'}
                ],
                value='total_cases',
                labelStyle={'display': 'inline-block', 'marginRight': '10px'}
            )
        ])
    
    # Préparation du graphique temporel
    time_chart = None
    if date_col:
        time_chart = dcc.Graph(id='mpox-time-chart')
    
    # Interface pour les données mpox
    mpox_content = html.Div([
        # Filtres
        html.Div([
            html.Label("Sélectionner des pays:"),
            dcc.Dropdown(
                id='mpox-country-dropdown',
                options=[{'label': country, 'value': country} 
                        for country in sorted(mpox_df[country_col].unique())],
                value=mpox_df[country_col].value_counts().nlargest(5).index.tolist(),
                multi=True
            ),
            
            # Ajouter le filtre de métrique s'il est disponible
            metric_filter if metric_filter else None
        ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
        
        # Graphiques
        dcc.Graph(id='mpox-map'),
        dcc.Graph(id='mpox-bar-chart'),
        
        # Ajouter le graphique temporel s'il est disponible
        time_chart if time_chart else None
    ])
    
    return html.Div([
        html.H4("Données Mpox disponibles", style={'color': 'green'})
    ]), mpox_content

# Callback pour les graphiques Mpox
@app.callback(
    [Output('mpox-map', 'figure'),
     Output('mpox-bar-chart', 'figure')],
    [Input('mpox-country-dropdown', 'value')]
)
def update_mpox_graphs(countries):
    if mpox_df is None or mpox_df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Aucune donnée disponible")
        return empty_fig, empty_fig
    
    # Identifier les colonnes clés
    country_col = next((col for col in mpox_df.columns if col.lower() in ['country', 'location'] or 'country' in col.lower() or 'nation' in col.lower()), None)
    case_col = next((col for col in mpox_df.columns if col.lower() in ['cases', 'total_cases'] or 'case' in col.lower()), None)
    
    if country_col is None:
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Données non structurées")
        return empty_fig, empty_fig
    
    # Agréger les données par pays
    if case_col:
        # Utiliser la colonne de cas existante
        country_counts = mpox_df.groupby(country_col)[case_col].sum().reset_index()
        country_counts.columns = ['Country', 'Cases']
    else:
        # Compter le nombre d'occurrences
        country_counts = mpox_df[country_col].value_counts().reset_index()
        country_counts.columns = ['Country', 'Cases']
    
    # Filtrer par pays sélectionnés si spécifié
    if countries and len(countries) > 0:
        filtered_counts = country_counts[country_counts['Country'].isin(countries)]
    else:
        filtered_counts = country_counts.head(10)
    
    # Carte choroplèthe
    map_fig = px.choropleth(
        country_counts,
        locations='Country',
        locationmode='country names',
        color='Cases',
        title='Distribution mondiale des cas de Mpox',
        color_continuous_scale='Viridis'
    )
    
    # Graphique à barres
    bar_fig = px.bar(
        filtered_counts.sort_values('Cases', ascending=False),
        x='Country',
        y='Cases',
        title='Nombre de cas de Mpox par pays',
        color='Country'
    )
    
    return map_fig, bar_fig

# Callback pour le graphique d'évolution temporelle mpox (si présent)
@app.callback(
    Output('mpox-time-chart', 'figure'),
    [Input('mpox-country-dropdown', 'value')]
)
def update_mpox_time_chart(countries):
    # Si le callback est appelé mais que le graphique n'existe pas dans le layout,
    # Dash va ignorer silencieusement le callback
    if mpox_df is None or mpox_df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Aucune donnée disponible")
        return empty_fig
    
    # Identifier les colonnes clés
    country_col = next((col for col in mpox_df.columns if col.lower() in ['country', 'location'] or 'country' in col.lower() or 'nation' in col.lower()), None)
    date_col = next((col for col in mpox_df.columns if col.lower() in ['date_confirmation', 'date'] or 'date' in col.lower()), None)
    case_col = next((col for col in mpox_df.columns if col.lower() in ['cases', 'total_cases'] or 'case' in col.lower()), None)
    
    if country_col is None or date_col is None:
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Données temporelles non disponibles")
        return empty_fig
    
    time_fig = go.Figure()
    
    # Si aucun pays n'est sélectionné, prendre les 5 premiers pays
    if not countries or len(countries) == 0:
        countries = mpox_df[country_col].value_counts().nlargest(5).index.tolist()
    
    for country in countries:
        country_data = mpox_df[mpox_df[country_col] == country]
        if not country_data.empty:
            # Trier par date
            country_data = country_data.sort_values(date_col)
            
            # Sélectionner la colonne à afficher
            y_col = case_col if case_col else 'cases'
            if y_col not in country_data.columns and 'total_cases' in country_data.columns:
                y_col = 'total_cases'
            elif y_col not in country_data.columns and 'new_cases' in country_data.columns:
                # Calculer le cumulatif des nouveaux cas
                country_data = country_data.sort_values(date_col)
                country_data['cumulative_cases'] = country_data['new_cases'].cumsum()
                y_col = 'cumulative_cases'
            
            if y_col in country_data.columns:
                time_fig.add_trace(go.Scatter(
                    x=country_data[date_col],
                    y=country_data[y_col],
                    mode='lines',
                    name=country
                ))
    
    time_fig.update_layout(
        title='Évolution des cas de Mpox par pays',
        xaxis_title='Date',
        yaxis_title='Nombre de cas',
        template='plotly_white'
    )
    
    return time_fig

# Callback pour la comparaison
@app.callback(
    Output('comparison-chart', 'figure'),
    [Input('compare-country-dropdown', 'value')]
)
def update_comparison(countries):
    # Créer un graphique comparatif entre COVID-19 et Mpox
    
    fig = go.Figure()
    
    # Si aucun pays n'est sélectionné, utiliser quelques pays par défaut
    if not countries or len(countries) == 0:
        countries = ['France', 'United States', 'Germany']
    
    # Ajouter les données COVID
    for country in countries:
        country_data = covid_df[covid_df['location'] == country]
        if not country_data.empty:
            fig.add_trace(go.Scatter(
                x=country_data['date'],
                y=country_data['total_cases'],
                mode='lines',
                name=f"{country} - COVID-19"
            ))
    
    # Ajouter les données Mpox si disponibles
    if mpox_df is not None and not mpox_df.empty:
        # Identifier les colonnes clés
        country_col = next((col for col in mpox_df.columns if col.lower() in ['country', 'location'] or 'country' in col.lower() or 'nation' in col.lower()), None)
        date_col = next((col for col in mpox_df.columns if col.lower() in ['date_confirmation', 'date'] or 'date' in col.lower()), None)
        case_col = next((col for col in mpox_df.columns if col.lower() in ['cases', 'total_cases'] or 'case' in col.lower()), None)
        
        if country_col is not None and date_col is not None:
            for country in countries:
                # Filtrer les données par pays
                matching_countries = []
                
                # Correspondance exacte
                if country in mpox_df[country_col].values:
                    matching_countries = [country]
                else:
                    # Essayer des correspondances partielles
                    matching_countries = [c for c in mpox_df[country_col].unique() 
                                          if country.lower() in c.lower() or c.lower() in country.lower()]
                
                if not matching_countries:
                    continue
                    
                for match_country in matching_countries[:1]:  # Limiter à une correspondance
                    country_data = mpox_df[mpox_df[country_col] == match_country]
                    if country_data.empty:
                        continue
                        
                    # Sélectionner et préparer les données pour le graphique
                    try:
                        # Trier par date
                        country_data = country_data.sort_values(date_col)
                        
                        # Sélectionner la colonne de cas appropriée
                        if case_col and case_col in country_data.columns:
                            y_values = country_data[case_col]
                        elif 'total_cases' in country_data.columns:
                            y_values = country_data['total_cases']
                        elif 'new_cases' in country_data.columns:
                            # Calculer le cumulatif
                            y_values = country_data['new_cases'].cumsum()
                        else:
                            # Compter par date
                            date_counts = country_data.groupby(date_col).size()
                            dates = date_counts.index
                            y_values = date_counts.values
                            
                            fig.add_trace(go.Scatter(
                                x=dates,
                                y=y_values,
                                mode='lines',
                                name=f"{country} - Mpox",
                                line=dict(dash='dash')
                            ))
                            continue
                        
                        # Ajouter la trace avec les valeurs calculées
                        fig.add_trace(go.Scatter(
                            x=country_data[date_col],
                            y=y_values,
                            mode='lines',
                            name=f"{country} - Mpox",
                            line=dict(dash='dash')
                        ))
                        
                    except Exception as e:
                        print(f"Erreur lors de l'ajout des données mpox pour {country}: {e}")
    
    fig.update_layout(
        title='Comparaison COVID-19 vs Mpox par pays',
        xaxis_title='Date',
        yaxis_title='Nombre de cas',
        legend_title='Pays et maladie',
        template='plotly_white'
    )
    
    # Utiliser une échelle logarithmique pour mieux voir les deux maladies
    fig.update_yaxes(type='log')
    
    return fig

# Lancement de l'application
if __name__ == '__main__':
    print("Démarrage du dashboard...")
    app.run(debug=True)
else:
    # Cette partie est exécutée lorsque le module est importé
    # Ajouter des messages de débogage
    print("Le module dashboard.py a été importé")
    print("Structure des données mpox:")
    if mpox_df is not None:
        print(f"Colonnes: {mpox_df.columns.tolist()}")
        print(f"Nombre de lignes: {len(mpox_df)}")
        print(f"Premières lignes: \n{mpox_df.head(2)}")
    else:
        print("Aucune donnée mpox disponible")
        
    print("Structure des données COVID:")
    print(f"Colonnes: {covid_df.columns.tolist()}")
    print(f"Nombre de lignes: {len(covid_df)}")
    print(f"Premières lignes: \n{covid_df.head(2)}") 