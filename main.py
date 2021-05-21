import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import countries_df, totals_df
from builders import make_table

stylesheets = ["https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
               "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap"]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=stylesheets)

bubble_map = px.scatter_geo(countries_df,
                            size="Confirmed",
                            size_max=40,
                            hover_name="Country_Region",
                            locations="Country_Region",
                            locationmode="country names",
                            color="Confirmed",
                            template="plotly_dark",
                            title="Confirmed By County",
                            color_continuous_scale=px.colors.sequential.Oryel,
                            projection="natural earth",
                            hover_data={
                                "Confirmed": ":,2f",
                                "Deaths": ":,2f",
                                "Recovered": ":,2f",
                                "Country_Region": False
                            })

bubble_map.update_layout(
    # l => left, r => rigth, t => top b => bottom
    margin=dict(l=0, r=0, t=50, b=0)
)

bars_graph = px.bar(totals_df, hover_data={
    "count": ":,"
},  x="condition", y="count", title="Total Global Cases")

bars_graph.update_layout(
    xaxis=dict(title="Conditon"),
    yaxis=dict(title="Count")
)

app.layout = html.Div(
    style={
        "minHeight": "100vh", "backgroundColor": "#111111", "color": "white", "fontFamily": "Open Sans , sans-serif"},
    children=[
        html.Header(
            style={'textAlign': 'center',
                   "paddingTop": "50px", "marginBottom": 100},
            children=[
                html.H1("Corona DashBorad", style={"fontSize": "30px"})]
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(figure=bubble_map)
                    ]
                ),
                html.Div(
                    children=[
                        make_table(countries_df)
                    ]
                ),
                
            ]
        ),
        html.Div(
            children=[
                html.Div(children=[dcc.Graph(figure=bars_graph)])]
        )
    ],
)


if __name__ == '__main__':
    app.run_server(debug=True)
