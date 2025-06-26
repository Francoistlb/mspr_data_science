#!/usr/bin/env python3
"""
Dashboard COVID-19 & Mpox - Version Finale
Auteur: Assistant IA
Date: 2024
"""

import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DashboardCOVIDMpox:
    """Classe principale du dashboard COVID-19 & Mpox"""
    
    def __init__(self):
        """Initialisation du dashboard"""
        self.covid_df = None
        self.mpox_df = None
        self.app = None
        self.colors = {
            'background': '#f8f9fa',
            'text': '#2c3e50',
            'primary': '#3498db',
            'secondary': '#e74c3c',
            'success': '#27ae60',
            'warning': '#f39c12'
        }
        
        self._load_data()
        self._create_app()
        self._setup_layout()
        self._setup_callbacks()
    
    def _load_data(self):
        """Charger les données COVID-19 et Mpox"""
        try:
            # Vérifier si les données existent
            if not os.path.exists('data/covid_processed.csv'):
                logger.error("Fichier covid_processed.csv non trouvé")
                return
            
            if not os.path.exists('data/mpox_processed.csv'):
                logger.warning("Fichier mpox_processed.csv non trouvé - données Mpox non disponibles")
            
            # Charger les données COVID-19
            self.covid_df = pd.read_csv('data/covid_processed.csv')
            self.covid_df['date'] = pd.to_datetime(self.covid_df['date'], errors='coerce')
            logger.info(f"Données COVID-19 chargées: {len(self.covid_df)} lignes")
            
            # Charger les données Mpox si disponibles
            if os.path.exists('data/mpox_processed.csv'):
                self.mpox_df = pd.read_csv('data/mpox_processed.csv')
                if 'date' in self.mpox_df.columns:
                    self.mpox_df['date'] = pd.to_datetime(self.mpox_df['date'], errors='coerce')
                logger.info(f"Données Mpox chargées: {len(self.mpox_df)} lignes")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données: {e}")
    
    def _create_app(self):
        """Créer l'application Dash"""
        self.app = dash.Dash(
            __name__,
            title="Dashboard COVID-19 & Mpox",
            external_stylesheets=[
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
            ],
            suppress_callback_exceptions=True
        )
    
    def _setup_layout(self):
        """Configurer le layout du dashboard"""
        if self.covid_df is None:
            self.app.layout = html.Div([
                html.H1("Erreur de chargement des données", style={'color': 'red', 'textAlign': 'center'}),
                html.P("Les données COVID-19 n'ont pas pu être chargées. Vérifiez que le fichier covid_processed.csv existe.")
            ])
            return
        
        # Obtenir la liste des pays disponibles
        countries = sorted(self.covid_df['location'].unique())
        countries = [c for c in countries if pd.notna(c)]
        
        # Pays par défaut
        default_countries = ['France', 'United States', 'Germany', 'China', 'Brazil']
        available_defaults = [c for c in default_countries if c in countries]
        if not available_defaults:
            available_defaults = countries[:5] if len(countries) >= 5 else countries
        
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1([
                    html.I(className="fas fa-chart-line", style={'marginRight': '10px'}),
                    "Dashboard COVID-19 & Mpox"
                ], style={'textAlign': 'center', 'color': self.colors['text'], 'marginBottom': '30px'})
            ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            
            # Filtres globaux
            html.Div([
                html.H3("Filtres", style={'color': self.colors['text'], 'marginBottom': '15px'}),
                
                html.Div([
                    # Filtre pays
                    html.Div([
                        html.Label("Pays:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                        dcc.Dropdown(
                            id='country-filter',
                            options=[{'label': country, 'value': country} for country in countries],
                            value=available_defaults,
                            multi=True,
                            placeholder="Sélectionner des pays...",
                            style={'marginBottom': '15px'}
                        )
                    ], style={'flex': '1', 'marginRight': '20px'}),
                    
                    # Filtre période
                    html.Div([
                        html.Label("Période:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                        dcc.DatePickerRange(
                            id='date-filter',
                            min_date_allowed=self.covid_df['date'].min(),
                            max_date_allowed=self.covid_df['date'].max(),
                            start_date=self.covid_df['date'].min(),
                            end_date=self.covid_df['date'].max(),
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
                        html.H3("Évolution des cas COVID-19", style={'color': self.colors['text'], 'marginBottom': '15px'}),
                        dcc.Graph(id='covid-evolution-chart', style={'height': '400px'})
                    ], style={'flex': '1', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginRight': '10px'}),
                    
                    # Nombre de vaccinés par pays
                    html.Div([
                        html.H3("Nombre de vaccinés par pays", style={'color': self.colors['text'], 'marginBottom': '15px'}),
                        dcc.Graph(id='vaccination-chart', style={'height': '400px'})
                    ], style={'flex': '1', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginLeft': '10px'})
                ], style={'display': 'flex', 'marginBottom': '20px'}),
                
                # Deuxième ligne : Cas Mpox et Comparaison
                html.Div([
                    # Cas totaux Mpox par pays
                    html.Div([
                        html.H3("Cas totaux Mpox par pays", style={'color': self.colors['text'], 'marginBottom': '15px'}),
                        dcc.Graph(id='mpox-chart', style={'height': '400px'})
                    ], style={'flex': '1', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginRight': '10px'}),
                    
                    # Comparaison COVID vs Mpox
                    html.Div([
                        html.H3("Comparaison COVID vs Mpox", style={'color': self.colors['text'], 'marginBottom': '15px'}),
                        dcc.Graph(id='comparison-chart', style={'height': '400px'})
                    ], style={'flex': '1', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginLeft': '10px'})
                ], style={'display': 'flex'})
            ]),
            
            # Footer avec statistiques
            html.Div([
                html.H3("Statistiques globales", style={'color': self.colors['text'], 'marginBottom': '15px'}),
                html.Div(id='global-stats', style={'display': 'flex', 'justifyContent': 'space-around'})
            ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginTop': '20px'})
        ], style={'backgroundColor': self.colors['background'], 'padding': '20px', 'minHeight': '100vh'})
    
    def _setup_callbacks(self):
        """Configurer les callbacks Dash"""
        @self.app.callback(
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
            """Mettre à jour tous les graphiques"""
            try:
                if not countries or self.covid_df is None:
                    return self._create_empty_figures()
                
                # Conversion des dates
                start_date = pd.to_datetime(start_date) if start_date else self.covid_df['date'].min()
                end_date = pd.to_datetime(end_date) if end_date else self.covid_df['date'].max()
                
                # Filtrage des données COVID
                filtered_covid = self.covid_df[
                    (self.covid_df['location'].isin(countries)) & 
                    (self.covid_df['date'] >= start_date) & 
                    (self.covid_df['date'] <= end_date)
                ]
                
                # Créer les graphiques
                covid_evolution = self._create_covid_evolution_chart(filtered_covid)
                vaccination_chart = self._create_vaccination_chart(filtered_covid)
                mpox_chart = self._create_mpox_chart(countries)
                comparison_chart = self._create_comparison_chart(filtered_covid, countries)
                stats = self._create_global_stats(filtered_covid)
                
                return covid_evolution, vaccination_chart, mpox_chart, comparison_chart, stats
                
            except Exception as e:
                logger.error(f"Erreur dans update_charts: {e}")
                return self._create_empty_figures()
    
    def _create_empty_figures(self):
        """Créer des graphiques vides en cas d'erreur"""
        empty_fig = px.bar(title="Aucune donnée disponible")
        empty_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        return empty_fig, empty_fig, empty_fig, empty_fig, []
    
    def _create_covid_evolution_chart(self, filtered_covid):
        """Créer le graphique d'évolution COVID-19"""
        if filtered_covid.empty:
            return px.bar(title="Aucune donnée COVID-19 disponible")
        
        fig = px.line(
            filtered_covid,
            x='date',
            y='total_cases',
            color='location',
            title="Évolution des cas COVID-19",
            labels={'total_cases': 'Cas totaux', 'date': 'Date', 'location': 'Pays'}
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': self.colors['text']},
            hovermode='x unified'
        )
        return fig
    
    def _create_vaccination_chart(self, filtered_covid):
        """Créer le graphique de vaccination"""
        if filtered_covid.empty:
            return px.bar(title="Aucune donnée de vaccination disponible")
        
        latest_covid = filtered_covid.sort_values('date').groupby('location').last().reset_index()
        vaccination_data = latest_covid[
            latest_covid['people_vaccinated'].notna() & 
            (latest_covid['people_vaccinated'] > 0)
        ]
        
        if vaccination_data.empty:
            return px.bar(title="Aucune donnée de vaccination disponible")
        
        fig = px.bar(
            vaccination_data,
            x='people_vaccinated',
            y='location',
            orientation='h',
            title="Nombre de vaccinés par pays",
            labels={'people_vaccinated': 'Nombre de vaccinés', 'location': 'Pays'},
            color='people_vaccinated',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': self.colors['text']},
            yaxis={'categoryorder': 'total ascending'}
        )
        return fig
    
    def _create_mpox_chart(self, countries):
        """Créer le graphique Mpox"""
        if self.mpox_df is None or self.mpox_df.empty:
            return px.bar(title="Données Mpox non disponibles")
        
        available_countries = [c for c in countries if c in self.mpox_df['location'].unique()]
        if not available_countries:
            return px.bar(title="Aucune donnée Mpox disponible pour les pays sélectionnés")
        
        filtered_mpox = self.mpox_df[self.mpox_df['location'].isin(available_countries)]
        mpox_by_country = filtered_mpox.groupby('location')['total_cases'].sum().reset_index()
        
        fig = px.bar(
            mpox_by_country,
            x='location',
            y='total_cases',
            title="Cas totaux Mpox par pays",
            labels={'total_cases': 'Cas totaux', 'location': 'Pays'},
            color='total_cases',
            color_continuous_scale='Reds'
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': self.colors['text']},
            xaxis={'categoryorder': 'total descending'}
        )
        return fig
    
    def _create_comparison_chart(self, filtered_covid, countries):
        """Créer le graphique de comparaison"""
        if filtered_covid.empty:
            return px.bar(title="Aucune donnée de comparaison disponible")
        
        if self.mpox_df is None or self.mpox_df.empty:
            return px.bar(title="Données de comparaison non disponibles")
        
        # Préparer les données COVID
        latest_covid = filtered_covid.sort_values('date').groupby('location').last().reset_index()
        covid_latest = latest_covid[['location', 'total_cases']].rename(columns={'total_cases': 'covid_cases'})
        
        # Préparer les données Mpox
        available_countries = [c for c in countries if c in self.mpox_df['location'].unique()]
        if not available_countries:
            return px.bar(title="Aucune donnée de comparaison disponible")
        
        mpox_latest = self.mpox_df[self.mpox_df['location'].isin(available_countries)].groupby('location')['total_cases'].sum().reset_index()
        mpox_latest = mpox_latest.rename(columns={'total_cases': 'mpox_cases'})
        
        # Fusionner les données
        comparison_data = covid_latest.merge(mpox_latest, on='location', how='inner')
        
        if comparison_data.empty:
            return px.bar(title="Aucune donnée de comparaison disponible")
        
        # Créer le graphique combiné
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=comparison_data['location'],
            y=comparison_data['covid_cases'],
            name='COVID-19',
            marker_color=self.colors['primary']
        ))
        
        fig.add_trace(go.Bar(
            x=comparison_data['location'],
            y=comparison_data['mpox_cases'],
            name='Mpox',
            marker_color=self.colors['secondary']
        ))
        
        fig.update_layout(
            title="Comparaison COVID-19 vs Mpox par pays",
            barmode='group',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': self.colors['text']},
            xaxis={'title': 'Pays'},
            yaxis={'title': 'Nombre de cas'}
        )
        return fig
    
    def _create_global_stats(self, filtered_covid):
        """Créer les statistiques globales"""
        if filtered_covid.empty:
            return []
        
        try:
            total_cases = filtered_covid['total_cases'].max()
            total_deaths = filtered_covid['total_deaths'].max()
            total_vaccinated = filtered_covid['people_vaccinated'].max()
            
            stats = [
                html.Div([
                    html.H4(f"{total_cases:,.0f}", style={'color': self.colors['primary'], 'margin': '0'}),
                    html.P("Cas COVID-19", style={'margin': '0', 'fontSize': '14px'})
                ], style={'textAlign': 'center', 'padding': '10px'}),
                html.Div([
                    html.H4(f"{total_deaths:,.0f}", style={'color': self.colors['secondary'], 'margin': '0'}),
                    html.P("Décès COVID-19", style={'margin': '0', 'fontSize': '14px'})
                ], style={'textAlign': 'center', 'padding': '10px'}),
                html.Div([
                    html.H4(f"{total_vaccinated:,.0f}", style={'color': self.colors['success'], 'margin': '0'}),
                    html.P("Vaccinés", style={'margin': '0', 'fontSize': '14px'})
                ], style={'textAlign': 'center', 'padding': '10px'})
            ]
            return stats
        except Exception as e:
            logger.error(f"Erreur lors de la création des statistiques: {e}")
            return []
    
    def run(self, debug=True, host='0.0.0.0', port=8050):
        """Lancer le dashboard"""
        logger.info(f"Démarrage du dashboard sur http://{host}:{port}")
        self.app.run(debug=debug, host=host, port=port)

def main():
    """Fonction principale"""
    try:
        dashboard = DashboardCOVIDMpox()
        dashboard.run()
    except Exception as e:
        logger.error(f"Erreur lors du lancement du dashboard: {e}")
        print(f"Erreur: {e}")

if __name__ == '__main__':
    main() 