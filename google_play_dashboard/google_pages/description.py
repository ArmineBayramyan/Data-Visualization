from dash import html, register_page, dash_table, dcc
import dash_bootstrap_components as dbc
import pandas as pd

register_page(__name__, path="/", name="📄 Data Description", title="Google Play - Data Description")

# Load data
apps = pd.read_csv("data/cleaned_googleplaystore.csv")
user_reviews = pd.read_csv("data/cleaned_googleplaystore_user_reviews.csv")

layout = dbc.Container([
    html.H2("Google Play Store Dashboard: Dataset Description", className="my-4"),

    # Dataset 1 Description
    dbc.Card([
        dbc.CardHeader("📁 Dataset 1: googleplaystore.csv"),
        dbc.CardBody([
            html.Ul([
                html.Li([html.B("App"), ": Name of the application."]),
                html.Li([html.B("Category"), ": The category to which the app belongs."]),
                html.Li([html.B("Rating"), ": Overall user rating of the app (as when scraped)."]),
                html.Li([html.B("Reviews"), ": Total number of user reviews (as when scraped)."]),
                html.Li([html.B("Size"), ": Size of the app (as when scraped)."]),
                html.Li([html.B("Installs"), ": Number of downloads/installs (as when scraped)."]),
                html.Li([html.B("Type"), ": Specifies if the app is Free or Paid."]),
                html.Li([html.B("Price"), ": Price of the app (as when scraped)."]),
                html.Li([html.B("Content Rating"), ": Age group of the target audience (e.g., Children, Adult, etc.)."]),
                html.Li([html.B("Genres"), ": Apps may belong to multiple genres (e.g., Music & Family)."]),
                html.Li([html.B("Last Updated"), ": The date when the app was last updated."]),
                html.Li([html.B("Current Ver"), ": The current version of the app."]),
                html.Li([html.B("Android Ver"), ": The minimum Android version required to run the app."]),
                html.Li([html.B("Installs_category"), ": A label describing install volume (e.g., Moderate, Top Notch)."])
            ])
        ])
    ], className="mb-4"),

    # Dataset 1 Preview
    dbc.Card([
        dbc.CardHeader("🔍 Preview: googleplaystore.csv"),
        dbc.CardBody([
            dash_table.DataTable(
                data=apps.head(5).to_dict('records'),
                columns=[{"name": col, "id": col} for col in apps.columns],
                style_table={'overflowX': 'auto'},
                page_size=5,
                style_cell={'textAlign': 'left', 'padding': '5px', 'minWidth': '100px', 'maxWidth': '300px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            )
        ])
    ], className="mb-4"),

    # Dataset 2 Description
    dbc.Card([
        dbc.CardHeader("💬 Dataset 2: googleplaystore_user_reviews.csv"),
        dbc.CardBody([
            html.P("Each app contains up to 100 translated and preprocessed user reviews. The columns include:"),
            html.Ul([
                html.Li([html.B("App"), ": Name of the application."]),
                html.Li([html.B("Translated_Review"), ": Preprocessed and translated user review."]),
                html.Li([html.B("Sentiment"), ": Review sentiment — Positive, Negative, or Neutral."]),
                html.Li([html.B("Sentiment_Polarity"), ": Numeric score indicating sentiment strength (positive, negative, neutral)."]),
                html.Li([html.B("Sentiment_Subjectivity"), ": Score for subjectivity (close to 1 = opinion, close to 0 = fact)."])
            ])
        ])
    ], className="mb-4"),

    # Dataset 2 Preview
    dbc.Card([
        dbc.CardHeader("🔍 Preview: googleplaystore_user_reviews.csv"),
        dbc.CardBody([
            dash_table.DataTable(
                data=user_reviews.head(5).to_dict('records'),
                columns=[{"name": col, "id": col} for col in user_reviews.columns],
                style_table={'overflowX': 'auto'},
                page_size=5,
                style_cell={'textAlign': 'left', 'padding': '5px', 'minWidth': '100px', 'maxWidth': '300px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            )
        ])
    ], className="mb-4"),

    html.Hr(),
    html.P("This dashboard explores trends in app popularity, size, pricing, downloads, and user sentiment to derive insights from Google Play Store apps.",
           className="text-muted")
], fluid=True)
