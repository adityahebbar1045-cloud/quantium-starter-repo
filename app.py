from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# 1. Initialize the Dash app
app = Dash(__name__)

# 2. Load and prepare the data
# Using the filename we found in your 'ls' command earlier
df = pd.read_csv("formatted_sales_data.csv")

# Ensure the date is in the right format and sorted for a smooth line
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by="date")

# 3. Define the layout (The HTML structure)
app.layout = html.Div(style={'fontFamily': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif', 'padding': '40px', 'backgroundColor': '#f9f9f9'}, children=[
    
    html.H1(
        children='Pink Morsel Sales Visualiser',
        style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '10px'}
    ),

    html.P(
        children='Analyzing the impact of the January 15, 2021 price increase on total sales.',
        style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '1.1em'}
    ),

    # Region Selection Radio Buttons
    html.Div(style={'textAlign': 'center', 'margin': '30px', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
        html.Label("Filter by Region: ", style={'fontWeight': 'bold', 'marginRight': '15px'}),
        dcc.RadioItems(
            id='region-filter',
            options=[
                {'label': ' North ', 'value': 'north'},
                {'label': ' South ', 'value': 'south'},
                {'label': ' East ', 'value': 'east'},
                {'label': ' West ', 'value': 'west'},
                {'label': ' All Regions ', 'value': 'all'}
            ],
            value='all', 
            inline=True,
            inputStyle={"margin-left": "20px", "margin-right": "5px"}
        ),
    ]),

    # The Graph Container
    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
        dcc.Graph(id='sales-line-chart')
    ])
])

# 4. The Interactive Logic (Callback)
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_graph(selected_region):
    # Filter logic
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]

    # Create the line chart
    fig = px.line(
        filtered_df, 
        x="date", 
        y="sales", 
        title=f"Sales Performance - {selected_region.upper()}",
        template="plotly_white"
    )

    # Add the "Price Increase" reference line (January 15, 2021)
    fig.add_vline(x="2021-01-15", line_dash="dash", line_color="red")
    fig.add_annotation(x="2021-01-15", text="Price Increase", showarrow=False, yshift=10, font_color="red")

    fig.update_layout(
        xaxis_title="Timeline",
        yaxis_title="Total Sales (USD)",
        transition_duration=500
    )
    
    return fig

# 5. The Final Run Command (Updated for Modern Dash)
if __name__ == '__main__':
    app.run(debug=True)