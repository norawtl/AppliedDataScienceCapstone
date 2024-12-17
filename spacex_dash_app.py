# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Dropdown for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS SLC 40', 'value': 'CCAFS SLC 40'},
            {'label': 'KSC LC 39A', 'value': 'KSC LC 39A'},
            {'label': 'CCAFS LC 40', 'value': 'CCAFS LC 40'},
            {'label': 'VAFB SLC 4E', 'value': 'VAFB SLC 4E'}
        ],
        value='ALL',
        placeholder="Please select a launch site here",
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie chart for launch success counts
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Payload Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: str(i) for i in range(0, 10001, 2500)},
        value=[0, 10000]  # Default range
    ),

    html.Br(),

    # TASK 4: Scatter chart for Payload vs. Launch Success
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])


# TASK 2: Callback function for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # For all sites: show overall success vs failure
        fig = px.pie(
            spacex_df,
            names='class',  # 'class' column contains success (1) and failure (0)
            title='Total Success and Failure Launches for All Sites'
        )
    else:
        # Filter for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Success and Failure Launches for {entered_site}'
        )
    return fig


# TASK 4: Callback function for scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    # Filter payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site == 'ALL':
        # For all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation Between Payload and Success for All Sites'
        )
    else:
        # Filter for the selected site
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation Between Payload and Success for {entered_site}'
        )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
