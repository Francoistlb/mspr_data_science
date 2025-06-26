import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Dictionnaire de traduction pour les métriques
METRIC_LABELS = {
    "total_cases": "Cas totaux",
    "new_cases": "Nouveaux cas",
    "total_deaths": "Décès totaux",
    "new_deaths": "Nouveaux décès",
    "hosp_patients": "Hospitalisations",
    "cases": "Cas",
    "deaths": "Décès"
}

def metric_label(metric):
    return METRIC_LABELS.get(metric, metric.replace("_", " ").capitalize())

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
    html.H1("Dashboard COVID-19 et Mpox", className="header-title"),
    
    # Sélection des onglets
    dcc.Tabs([
        # Onglet COVID-19
        dcc.Tab(label="COVID-19", children=[
            html.Div([
                html.H3("Analyse COVID-19"),
                
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
                ], className="dash-container"),
                
                # Graphiques - Première ligne
                html.Div([
                    # Évolution temporelle
                    html.Div([
                        dcc.Graph(id='covid-line-chart')
                    ], style={'flex': '1', 'marginRight': '10px'}),
                    
                    # Dernières valeurs
                    html.Div([
                        dcc.Graph(id='covid-bar-chart')
                    ], style={'flex': '1', 'marginLeft': '10px'})
                ], style={'display': 'flex', 'marginBottom': '20px'}),
                
                # Graphiques - Deuxième ligne
                html.Div([
                    # Carte mondiale
                    html.Div([
                        dcc.Graph(id='covid-map')
                    ], style={'flex': '1', 'marginRight': '10px'}),
                    
                    # Barres par pays (comparaison)
                    html.Div([
                        dcc.Graph(id='covid-comparison-bars')
                    ], style={'flex': '1', 'marginLeft': '10px'})
                ], style={'display': 'flex', 'marginBottom': '20px'}),
                
                # Statistiques
                html.Div(id='covid-stats', className="dash-container")
            ])
        ]),
        
        # Onglet Mpox
        dcc.Tab(label="Mpox", children=[
            html.Div([
                html.H3("Analyse Mpox"),
                
                # Message si les données ne sont pas disponibles
                html.Div(id='mpox-data-status'),
                
                # Filtres (conditionnels selon disponibilité des données)
                html.Div(id='mpox-filters', className="dash-container"),
                
                # Graphiques - Première ligne
                html.Div([
                    # Évolution temporelle
                    html.Div([
                        dcc.Graph(id='mpox-line-chart')
                    ], style={'flex': '1', 'marginRight': '10px'}),
                    
                    # Dernières valeurs
                    html.Div([
                        dcc.Graph(id='mpox-bar-chart')
                    ], style={'flex': '1', 'marginLeft': '10px'})
                ], style={'display': 'flex', 'marginBottom': '20px'}),
                
                # Graphiques - Deuxième ligne
                html.Div([
                    # Carte mondiale
                    html.Div([
                        dcc.Graph(id='mpox-map')
                    ], style={'flex': '1', 'marginRight': '10px'}),
                    
                    # Barres par pays (comparaison)
                    html.Div([
                        dcc.Graph(id='mpox-comparison-bars')
                    ], style={'flex': '1', 'marginLeft': '10px'})
                ], style={'display': 'flex', 'marginBottom': '20px'}),
                
                # Statistiques
                html.Div(id='mpox-stats', className="dash-container")
            ])
        ]),
        
        # Onglet Comparatif
        dcc.Tab(label="Comparaison", children=[
            html.Div([
                html.H3("Comparaison COVID-19 vs Mpox"),
                html.Div([
                    html.Label("Sélectionner des pays:"),
                    dcc.Dropdown(
                        id='compare-country-dropdown',
                        options=[{'label': country, 'value': country} 
                                for country in sorted(covid_df['location'].unique())],
                        value=['France', 'United States', 'Germany'],
                        multi=True
                    ),
                    html.Label("Sélectionner une métrique:"),
                    dcc.RadioItems(
                        id='compare-metric-radio',
                        options=[
                            {'label': metric_label('total_cases'), 'value': 'total_cases'},
                            {'label': metric_label('new_cases'), 'value': 'new_cases'},
                            {'label': metric_label('total_deaths'), 'value': 'total_deaths'},
                            {'label': metric_label('new_deaths'), 'value': 'new_deaths'}
                        ],
                        value='total_cases',
                        labelStyle={'display': 'inline-block', 'marginRight': '10px'}
                    ),
                ], className="dash-container"),
                # Graphiques
                html.Div([
                    dcc.Graph(id='comparison-curve'),
                ], className="dash-container"),
                html.Div([
                    dcc.Graph(id='comparison-bar'),
                ], className="dash-container"),
                html.Div(id='comparison-summary', className="dash-container")
            ])
        ])
    ])
])

# Callbacks pour COVID-19
@app.callback(
    [Output('covid-line-chart', 'figure'),
     Output('covid-bar-chart', 'figure'),
     Output('covid-map', 'figure'),
     Output('covid-comparison-bars', 'figure'),
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
        title=f"Évolution de {metric_label(metric)} par pays"
    )
    line_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    
    # Graphique à barres des dernières valeurs
    latest_data = filtered_df.sort_values('date').groupby('location').last().reset_index()
    bar_fig = px.bar(
        latest_data, 
        x='location', 
        y=metric,
        title=f"Dernières valeurs de {metric_label(metric)} par pays",
        color='location'
    )
    bar_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    
    # Carte mondiale
    map_data = latest_data.copy()
    map_fig = px.choropleth(
        map_data,
        locations='location',
        locationmode='country names',
        color=metric,
        title=f'Distribution mondiale de {metric_label(metric)}',
        color_continuous_scale='Viridis'
    )
    map_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    
    # Barres de comparaison (tous les pays)
    all_countries_data = covid_df.sort_values('date').groupby('location').last().reset_index()
    comparison_fig = px.bar(
        all_countries_data.sort_values(metric, ascending=False).head(20),
        x='location',
        y=metric,
        title=f'Top 20 des pays par {metric_label(metric)}',
        color=metric,
        color_continuous_scale='Blues'
    )
    comparison_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    
    # Statistiques
    stats = []
    
    for country in countries:
        country_data = filtered_df[filtered_df['location'] == country]
        if not country_data.empty:
            latest_value = country_data.sort_values('date').iloc[-1][metric]
            max_value = country_data[metric].max()
            stats.append(html.Div([
                html.H4(country),
                html.P(f"Dernière valeur de {metric_label(metric)}: {latest_value:,.0f}"),
                html.P(f"Valeur maximale: {max_value:,.0f}")
            ]))
    
    return line_fig, bar_fig, map_fig, comparison_fig, stats

# Callback pour vérifier la disponibilité des données Mpox et générer les filtres
@app.callback(
    [Output('mpox-data-status', 'children'),
     Output('mpox-filters', 'children')],
    [Input('mpox-data-status', 'id')]  # Dummy input pour déclencher le callback au chargement
)
def check_mpox_data(_):
    if mpox_df is None or mpox_df.empty:
        return (
            html.Div([
                html.H4("Données Mpox non disponibles", className="status-error"),
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
                html.H4("Structure des données Mpox non reconnue", className="status-warning"),
                html.P("Le format des données mpox est différent de celui attendu.")
            ]),
            None
        )
    
    # Préparation des filtres pour les métriques
    metric_options = []
    if 'total_cases' in mpox_df.columns:
        metric_options.append({'label': 'Cas totaux', 'value': 'total_cases'})
    if 'new_cases' in mpox_df.columns:
        metric_options.append({'label': 'Nouveaux cas', 'value': 'new_cases'})
    if 'total_deaths' in mpox_df.columns:
        metric_options.append({'label': 'Décès totaux', 'value': 'total_deaths'})
    if 'new_deaths' in mpox_df.columns:
        metric_options.append({'label': 'Nouveaux décès', 'value': 'new_deaths'})
    
    if not metric_options:
        metric_options = [{'label': 'Cas', 'value': 'cases'}]
    
    # Interface pour les filtres mpox
    mpox_filters = html.Div([
        html.Label("Sélectionner des pays:"),
        dcc.Dropdown(
            id='mpox-country-dropdown',
            options=[{'label': country, 'value': country} 
                    for country in sorted(mpox_df[country_col].unique())],
            value=mpox_df[country_col].value_counts().nlargest(5).index.tolist(),
            multi=True
        ),
        
        html.Label("Sélectionner une métrique:"),
        dcc.RadioItems(
            id='mpox-metric-radio',
            options=metric_options,
            value=metric_options[0]['value'],
            labelStyle={'display': 'inline-block', 'marginRight': '10px'}
        ),
        
        html.Label("Plage de dates:"),
        dcc.DatePickerRange(
            id='mpox-date-picker',
            min_date_allowed=mpox_df[date_col].min() if date_col else None,
            max_date_allowed=mpox_df[date_col].max() if date_col else None,
            start_date=mpox_df[date_col].min() if date_col else None,
            end_date=mpox_df[date_col].max() if date_col else None
        )
    ])
    
    return None, mpox_filters

# Callback pour les graphiques Mpox harmonisés
@app.callback(
    [Output('mpox-line-chart', 'figure'),
     Output('mpox-bar-chart', 'figure'),
     Output('mpox-map', 'figure'),
     Output('mpox-comparison-bars', 'figure'),
     Output('mpox-stats', 'children')],
    [Input('mpox-country-dropdown', 'value'),
     Input('mpox-metric-radio', 'value'),
     Input('mpox-date-picker', 'start_date'),
     Input('mpox-date-picker', 'end_date')]
)
def update_mpox_graphs(countries, metric, start_date, end_date):
    if mpox_df is None or mpox_df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Aucune donnée disponible")
        return empty_fig, empty_fig, empty_fig, empty_fig, []
    
    # Identifier les colonnes clés
    country_col = next((col for col in mpox_df.columns if col.lower() in ['country', 'location'] or 'country' in col.lower() or 'nation' in col.lower()), None)
    date_col = next((col for col in mpox_df.columns if col.lower() in ['date_confirmation', 'date'] or 'date' in col.lower()), None)
    
    if country_col is None:
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Données non structurées")
        return empty_fig, empty_fig, empty_fig, empty_fig, []
    
    # Filtrer les données
    filtered_df = mpox_df[mpox_df[country_col].isin(countries)]
    if date_col and start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df[date_col] >= start_date) & 
            (filtered_df[date_col] <= end_date)
        ]
    
    if filtered_df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Aucune donnée disponible pour les filtres sélectionnés")
        return empty_fig, empty_fig, empty_fig, empty_fig, []
    
    # 1. Évolution temporelle
    if date_col and metric in filtered_df.columns:
        line_fig = px.line(
            filtered_df,
            x=date_col,
            y=metric,
            color=country_col,
            title=f"Évolution de {metric_label(metric)} par pays"
        )
        line_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    else:
        line_fig = go.Figure()
        line_fig.update_layout(title="Données temporelles non disponibles")
    
    # 2. Dernières valeurs par pays
    if metric in filtered_df.columns:
        latest_data = filtered_df.sort_values(date_col if date_col else country_col).groupby(country_col)[metric].last().reset_index()
        bar_fig = px.bar(
            latest_data,
            x=country_col,
            y=metric,
            title=f"Dernières valeurs de {metric_label(metric)} par pays",
            color=country_col
        )
        bar_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    else:
        bar_fig = go.Figure()
        bar_fig.update_layout(title="Métrique non disponible")
    
    # 3. Carte mondiale
    if metric in filtered_df.columns:
        map_data = latest_data if 'latest_data' in locals() else filtered_df.groupby(country_col)[metric].sum().reset_index()
        map_fig = px.choropleth(
            map_data,
            locations=country_col,
            locationmode='country names',
            color=metric,
            title=f'Distribution mondiale de {metric_label(metric)}',
            color_continuous_scale='Viridis'
        )
        map_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    else:
        map_fig = go.Figure()
        map_fig.update_layout(title="Carte non disponible")
    
    # 4. Barres de comparaison (tous les pays)
    all_countries_data = mpox_df.groupby(country_col)[metric].sum().reset_index() if metric in mpox_df.columns else mpox_df[country_col].value_counts().reset_index()
    if metric in mpox_df.columns:
        comparison_fig = px.bar(
            all_countries_data.sort_values(metric, ascending=False).head(20),
            x=country_col,
            y=metric,
            title=f'Top 20 des pays par {metric_label(metric)}',
            color=metric,
            color_continuous_scale='Reds'
        )
    else:
        comparison_fig = px.bar(
            all_countries_data.head(20),
            x=country_col,
            y='count',
            title='Top 20 des pays par nombre de cas',
            color='count',
            color_continuous_scale='Reds'
        )
    comparison_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    
    # 5. Statistiques
    stats = []
    for country in countries:
        country_data = filtered_df[filtered_df[country_col] == country]
        if not country_data.empty and metric in country_data.columns:
            latest_value = country_data.sort_values(date_col if date_col else country_col).iloc[-1][metric]
            max_value = country_data[metric].max()
            stats.append(html.Div([
                html.H4(country),
                html.P(f"Dernière valeur de {metric_label(metric)}: {latest_value:,.0f}"),
                html.P(f"Valeur maximale: {max_value:,.0f}")
            ]))
    
    return line_fig, bar_fig, map_fig, comparison_fig, stats

# Callback pour la comparaison
@app.callback(
    [Output('comparison-curve', 'figure'),
     Output('comparison-bar', 'figure'),
     Output('comparison-summary', 'children')],
    [Input('compare-country-dropdown', 'value'),
     Input('compare-metric-radio', 'value')]
)
def update_comparison(countries, metric):
    # Courbe d'évolution
    fig = go.Figure()
    for country in countries:
        country_data = covid_df[covid_df['location'] == country]
        if not country_data.empty and metric in country_data.columns:
            fig.add_trace(go.Scatter(
                x=country_data['date'],
                y=country_data[metric],
                mode='lines',
                name=f"{country} - COVID-19"
            ))
    if mpox_df is not None and not mpox_df.empty:
        country_col = next((col for col in mpox_df.columns if col.lower() in ['country', 'location'] or 'country' in col.lower() or 'nation' in col.lower()), None)
        date_col = next((col for col in mpox_df.columns if col.lower() in ['date_confirmation', 'date'] or 'date' in col.lower()), None)
        if country_col and date_col and metric in mpox_df.columns:
            for country in countries:
                for match_country in [c for c in mpox_df[country_col].unique() if country.lower() in c.lower() or c.lower() in country.lower()]:
                    country_data = mpox_df[mpox_df[country_col] == match_country]
                    if not country_data.empty:
                        fig.add_trace(go.Scatter(
                            x=country_data[date_col],
                            y=country_data[metric],
                            mode='lines',
                            name=f"{country} - Mpox",
                            line=dict(dash='dash')
                        ))
    fig.update_layout(
        title=f"Comparaison {metric_label(metric)} COVID-19 vs Mpox par pays",
        xaxis_title="Date",
        yaxis_title=metric_label(metric),
        legend_title="Pays et maladie",
        template='plotly_white',
        yaxis_type='log'
    )

    # Barres comparatives
    bar_data = []
    for country in countries:
        covid_val = covid_df[covid_df['location'] == country][metric].max() if not covid_df[covid_df['location'] == country].empty and metric in covid_df.columns else 0
        mpox_val = 0
        if mpox_df is not None and not mpox_df.empty:
            country_col = next((col for col in mpox_df.columns if col.lower() in ['country', 'location'] or 'country' in col.lower() or 'nation' in col.lower()), None)
            if country_col and metric in mpox_df.columns:
                for match_country in [c for c in mpox_df[country_col].unique() if country.lower() in c.lower() or c.lower() in country.lower()]:
                    mpox_val = mpox_df[mpox_df[country_col] == match_country][metric].max()
                    break
        bar_data.append({'Pays': country, 'COVID-19': covid_val, 'Mpox': mpox_val})
    bar_fig = go.Figure(data=[
        go.Bar(name='COVID-19', x=[d['Pays'] for d in bar_data], y=[d['COVID-19'] for d in bar_data]),
        go.Bar(name='Mpox', x=[d['Pays'] for d in bar_data], y=[d['Mpox'] for d in bar_data])
    ])
    bar_fig.update_layout(
        barmode='group',
        title=f"Comparatif {metric_label(metric)} COVID-19 vs Mpox par pays",
        yaxis_title=metric_label(metric),
        template='plotly_white',
        yaxis_type='log'
    )
    bar_fig.update_traces(texttemplate='%{y:.0f}', textposition='outside')

    # Résumé
    summary = html.Table([
        html.Thead(html.Tr([html.Th("Pays"), html.Th("COVID-19"), html.Th("Mpox")])),
        html.Tbody([
            html.Tr([
                html.Td(d['Pays']),
                html.Td(f"{d['COVID-19']:,}".replace(',', ' ')),
                html.Td(f"{d['Mpox']:,}".replace(',', ' '))
            ]) for d in bar_data
        ])
    ], style={'width': '100%', 'marginTop': '20px', 'textAlign': 'center'})

    return fig, bar_fig, summary

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