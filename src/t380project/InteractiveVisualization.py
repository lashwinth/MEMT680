import pandas as pd
import dash
import os
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Get the current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up one level to 'src'
src_dir = os.path.dirname(current_dir)

# Specify the relative path to the CSV file
file_path = os.path.join(src_dir, 'NBA_Dataset.csv')

# Check if the file exists
if os.path.isfile(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Initialize Dash
    app = dash.Dash(__name__)

    # Layout of the app
    app.layout = html.Div([
        html.H1("NBA Player Scatter Plot"),

        # Dropdown for player selection
        dcc.Dropdown(
            id='player-dropdown-scatter',
            options=[{'label': player, 'value': player} for player in df['player'].unique()],
            value='LeBron James',
            multi=False
        ),

        # Scatter Plot for selected player
        dcc.Graph(id='scatter-plot-scatter'),

    ])

    # Define callback to update scatter plot based on selected player
    @app.callback(
        Output('scatter-plot-scatter', 'figure'),
        [Input('player-dropdown-scatter', 'value')]
    )
    def update_scatter_plot(selected_player):
        # Filter Data for the selected player
        filtered_df = df[df['player'] == selected_player]

        # Scatter Plot
        scatter_fig = px.scatter(
            filtered_df,
            x='season',
            y='fg_per_g',
            title=f'Scatter Plot with Line for {selected_player}',
            labels={'season': 'Season', 'fg_per_g': 'Field Goals Per Game'},
            template='plotly'
        )

        # Add a line to the scatter plot
        scatter_fig.add_scatter(
            x=filtered_df['season'],
            y=filtered_df['fg_per_g'],
            mode='lines',
            line=dict(color='red', width=2),
            showlegend=False
        )

        return scatter_fig

    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)
