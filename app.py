from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# 1. Initialize Dash with a modern Font (Google Fonts)
app = Dash(__name__)

# 2. Data Setup
df = pd.read_csv("formatted_sales_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date")

# 3. Enhanced Layout with CSS styling
app.layout = html.Div(
    style={
        "backgroundColor": "#f4f7f6",
        "fontFamily": '"Open Sans", sans-serif',
        "padding": "50px",
        "minHeight": "100vh",
    },
    children=[
        # Header Section
        html.Div(
            style={
                "backgroundColor": "#2c3e50",
                "padding": "30px",
                "borderRadius": "15px",
                "boxShadow": "0 10px 30px rgba(0,0,0,0.1)",
                "marginBottom": "40px",
            },
            children=[
                html.H1(
                    "Pink Morsel Sales Performance",
                    style={
                        "color": "white",
                        "textAlign": "center",
                        "margin": "0",
                        "fontSize": "36px",
                    },
                ),
                html.P(
                    "Interactive Analytics Dashboard for Soul Foods Executives",
                    style={
                        "color": "#bdc3c7",
                        "textAlign": "center",
                        "marginTop": "10px",
                    },
                ),
            ],
        ),
        # Controls Section (The Radio Buttons)
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "25px",
                "borderRadius": "12px",
                "boxShadow": "0 4px 15px rgba(0,0,0,0.05)",
                "maxWidth": "800px",
                "margin": "0 auto 40px auto",
                "textAlign": "center",
            },
            children=[
                html.Label(
                    "Filter Analysis by Region",
                    style={
                        "fontWeight": "bold",
                        "display": "block",
                        "marginBottom": "15px",
                        "fontSize": "18px",
                        "color": "#34495e",
                    },
                ),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": " North ", "value": "north"},
                        {"label": " East ", "value": "east"},
                        {"label": " South ", "value": "south"},
                        {"label": " West ", "value": "west"},
                        {"label": " All Regions ", "value": "all"},
                    ],
                    value="all",
                    inline=True,
                    # Custom CSS for the radio items
                    labelStyle={
                        "margin": "0 15px",
                        "cursor": "pointer",
                        "fontSize": "16px",
                    },
                    inputStyle={"margin-right": "8px"},
                ),
            ],
        ),
        # Graph Section
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "15px",
                "boxShadow": "0 10px 25px rgba(0,0,0,0.1)",
            },
            children=[
                dcc.Graph(id="sales-line-chart", config={"displayModeBar": False})
            ],
        ),
    ],
)


# 4. Callback Logic
@app.callback(Output("sales-line-chart", "figure"), Input("region-filter", "value"))
def update_graph(selected_region):
    filtered_df = (
        df if selected_region == "all" else df[df["region"] == selected_region]
    )

    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title=f"Revenue Trend: {selected_region.upper()}",
        template="plotly_white",
        color_discrete_sequence=["#2980b9"],  # A nice professional blue
    )

    # Styling the chart lines and axes
    fig.add_vline(x="2021-01-15", line_dash="dash", line_color="#e74c3c", line_width=2)
    fig.add_annotation(
        x="2021-01-15",
        text="Price Increase",
        showarrow=False,
        yshift=15,
        font_color="#e74c3c",
    )

    fig.update_layout(
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Open Sans", size=14),
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
