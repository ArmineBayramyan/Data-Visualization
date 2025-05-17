from dash import html, dcc, register_page
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

register_page(__name__, path='/sentiment', name='🧠 User Sentiment', title='Google Play - Sentiment')

# Load both datasets
apps = pd.read_csv("data/cleaned_googleplaystore.csv")
user_reviews = pd.read_csv("data/cleaned_googleplaystore_user_reviews.csv")

# Merge them on App name
merged_df = pd.merge(apps, user_reviews, on="App")

# Metrics for KPI row
total_reviews = len(merged_df)
avg_polarity = merged_df['Sentiment_Polarity'].mean()
positive_ratio = (merged_df['Sentiment'] == 'Positive').mean()

# Layout
layout = dbc.Container([
    html.H2("User Sentiment Analysis", className="my-4"),

    # KPI Row
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("📝 Total Reviews", className="card-title"),
            html.P(f"{total_reviews:,}", className="card-text fs-4 fw-bold")
        ]), className="text-center shadow-sm"), md=4),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("😊 % Positive Reviews", className="card-title"),
            html.P(f"{positive_ratio * 100:.1f}%", className="card-text fs-4 fw-bold")
        ]), className="text-center shadow-sm"), md=4),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("📊 Avg. Sentiment Polarity", className="card-title"),
            html.P(f"{avg_polarity:.2f}", className="card-text fs-4 fw-bold")
        ]), className="text-center shadow-sm"), md=4)
    ], className="mb-4"),

    # Sentiment Distribution by Category
    dbc.Card([
        dbc.CardHeader("🧭 Sentiment Distribution by App Category"),
        dbc.CardBody([
            dcc.Graph(
                figure=px.histogram(
                    merged_df,
                    x='Category',
                    color='Sentiment',
                    barmode='group',
                    category_orders={
                        'Category': merged_df.groupby("Category").size().sort_values(ascending=False).index.tolist()
                    },
                    title='Sentiment Distribution by App Category (Sorted by Total Reviews)'
                ).update_layout(xaxis_tickangle=-45)
            ),
            html.P("""
                The sentiment analysis reveals that most app categories receive predominantly positive feedback,
                with GAME and FAMILY leading in total review volume. However, GAME also shows the highest number
                of negative reviews—likely due to its large user base and higher expectations.
            """)
        ])
    ], className="mb-4"),

    # Average Sentiment Polarity by Rating
    dbc.Card([
        dbc.CardHeader("📈 Average Sentiment Polarity by App Rating"),
        dbc.CardBody([
            dcc.Graph(
                figure=px.line(
                    merged_df.groupby('Rating')['Sentiment_Polarity'].mean().reset_index(),
                    x='Rating',
                    y='Sentiment_Polarity',
                    title='Average Sentiment Polarity by App Rating',
                    labels={'Rating': 'App Rating', 'Sentiment_Polarity': 'Average Sentiment Polarity'},
                    markers=True,
                    template='simple_white'
                ).update_layout(height=500)
            ),
            html.P("""
                Apps rated below 3.0 generally receive negative sentiment in reviews.
                Ratings above 4.0 tend to show a clear upward trend in review positivity.
                This suggests that better-rated apps also foster more favorable review language.
            """)
        ])
    ], className="mb-4"),

    # Average Sentiment Polarity by Category
    dbc.Card([
        dbc.CardHeader("📊 Average Sentiment Polarity by App Category"),
        dbc.CardBody([
            dcc.Graph(
                figure=px.bar(
                    merged_df.groupby('Category')['Sentiment_Polarity'].mean().sort_values().reset_index(),
                    x='Category',
                    y='Sentiment_Polarity',
                    title="Average Sentiment Polarity by App Category",
                    labels={'Sentiment_Polarity': 'Average Sentiment Polarity'},
                    template='simple_white'
                ).update_layout(xaxis_tickangle=90)
            ),
            html.P("""
                Categories like COMICS, EVENTS, and AUTO_AND_VEHICLES show the highest positivity.
                Meanwhile, GAME ranks lowest—reinforcing earlier findings that it's more polarizing.
                This suggests app type significantly influences user satisfaction patterns.
            """)
        ])
    ], className="mb-4"),

    html.Hr(),
    html.P("Overall, sentiment trends show a meaningful relationship between app rating, category, and review tone. "
           "Developers can use these insights to better understand their audience and improve engagement.",
           className="text-muted")
])

