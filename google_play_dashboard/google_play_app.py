import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Specify the correct folder where your pages live
app = dash.Dash(
    __name__,
    use_pages=True,
    pages_folder="google_pages",  
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

server = app.server

# Sidebar toggle button
toggle_button = dbc.Button("☰", color="primary", className="ms-2", id="toggle-button", n_clicks=0)

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            html.Div(page["name"], className="ms-2"),
            href=page["path"],
            active="exact"
        )
        for page in sorted(dash.page_registry.values(), key=lambda p: p["path"])
    ],
    vertical=True,
    pills=True,
    className="bg-light",
    id="sidebar"
)

# Layout with sidebar and page container
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Google Play Dashboard", className="text-center"),
            toggle_button
        ])
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([sidebar], width=2, id="sidebar-col"),
        dbc.Col([dash.page_container], width=10, id="content-col")
    ])
], fluid=True)

# Sidebar toggle callback
@app.callback(
    [dash.Output("sidebar-col", "width"),
     dash.Output("content-col", "width"),
     dash.Output("sidebar-col", "style")],
    [dash.Input("toggle-button", "n_clicks")],
    [dash.State("sidebar-col", "width")]
)
def toggle_sidebar(n_clicks, sidebar_width):
    if n_clicks:
        if sidebar_width == 2:
            return 0, 12, {"display": "none"}
        else:
            return 2, 10, {}
    return sidebar_width, 10, {}

if __name__ == '__main__':
    app.run(debug=True)
