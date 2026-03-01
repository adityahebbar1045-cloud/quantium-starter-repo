from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# 1. Load the cleaned data
df = pd.read_csv("formatted_sales_data.csv")

# Sort the dates so the line chart flows chronologically
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date")

# 2. Initialize the Dash app
app = Dash(__name__)

# 3. Define the layout (the frontend)
app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "textAlign": "center", "padding": "20px"},
    children=[
        html.H1("Soul Foods: Pink Morsel Sales", style={"color": "#333"}),
        html.P("Select a region to filter the sales data:", style={"fontSize": "18px"}),
        # Radio buttons for the region picker
        dcc.RadioItems(
            id="region-picker",
            options=[
                {"label": "North ", "value": "north"},
                {"label": "East ", "value": "east"},
                {"label": "South ", "value": "south"},
                {"label": "West ", "value": "west"},
                {"label": "All Regions", "value": "all"},
            ],
            value="all",  # Default value when the page loads
            inline=True,
            style={"fontSize": "16px", "margin": "20px"},
        ),
        # The graph component
        dcc.Graph(id="sales-line-chart"),
    ],
)


# 4. Define the callback (the interactive backend)
@app.callback(Output("sales-line-chart", "figure"), Input("region-picker", "value"))
def update_graph(selected_region):
    # Filter the dataframe based on the radio button selected
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    # Generate the line chart using Plotly Express
    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales - {selected_region.capitalize()} Region",
        color_discrete_sequence=["#E75480"],  # Pink color line
    )

    return fig


# 5. Run the local server
if __name__ == "__main__":
    app.run(debug=True)
