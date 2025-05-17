from dash import html, dcc, register_page, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

# Register this page
register_page(__name__, path="/overview", name="📊 App Overview", title="Google Play - Apps")

# Load cleaned app data
apps = pd.read_csv("data/cleaned_googleplaystore.csv")

# Precompute category counts
category_counts = (
    apps['Category']
    .value_counts()
    .reset_index()
    .rename(columns={'index': 'Category', apps['Category'].value_counts().name: 'Count'})
)

# Top 10 Categories by Installs
top_installs = apps.groupby('Category')['Installs'].sum().sort_values(ascending=False).head(10).reset_index()

# Top 10 Categories by Reviews
top_reviews = apps.groupby('Category')['Reviews'].sum().sort_values(ascending=False).head(10).reset_index()

layout = dbc.Container([
    html.H2("Google Play Store: App Overview", className="my-4"),

    # KPI Card: Total Apps
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📱 Total Apps", className="card-title"),
                    html.P(f"{len(apps):,}", className="card-text fs-4 fw-bold")
                ])
            ], className="text-center shadow-sm border-0")
        ], width=12)
    ], className="mb-4"),

    # Section: Apps per Category & Ratings
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📊 Number of Apps per Category"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.bar(
                            category_counts,
                            x="Category", y="Count",
                            title="Number of Apps per Category"
                        ).update_layout(xaxis_tickangle=-45, template="simple_white")
                    ),
                    html.P("Family and Game apps dominate the Play Store. Niche areas like Comics and Parenting offer opportunities for new developers.")
                ])
            ])
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("⭐ Distribution of App Ratings"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.histogram(apps.dropna(subset=["Rating"]), x="Rating", nbins=60, title="Distribution of App Ratings")
                        .add_shape(
                            type="line",
                            x0=apps["Rating"].mean(), x1=apps["Rating"].mean(),
                            y0=0, y1=1800,
                            line=dict(color="red", dash="dash", width=3)
                        )
                        .add_annotation(
                            x=apps["Rating"].mean(), y=1800,
                            text=f"Mean: {apps['Rating'].mean():.2f}",
                            showarrow=False, font=dict(color="red", size=12), xanchor="left"
                        )
                        .update_layout(template="simple_white")
                    ),
                    html.P("Ratings are highly skewed to the left—most apps score between 4.0 and 4.5, indicating generally positive reception.")
                ])
            ])
        ], md=6)
    ], className="mb-4"),


    # Tabbed Card: Size & Price vs Rating
    dbc.Card([
        dbc.CardHeader("📏 App Characteristics vs. Rating"),
        dbc.CardBody([
            dcc.Tabs(id="size-price-tabs", value="size", children=[
                dcc.Tab(label="📦 App Size vs Rating", value="size"),
                dcc.Tab(label="💰 Price vs Rating for Paid Apps", value="price"),
            ]),
            dcc.Graph(id="size-price-graph"),
            html.P(id="size-price-description", className="mt-2")
        ])
    ], className="mb-4"),

    # Section: Price Trend by Category
    dbc.Card([
        dbc.CardHeader("📈 App Pricing Trends by Category"),
        dbc.CardBody([
            dcc.Graph(
                figure=px.strip(apps[apps['Category'].isin(['GAME', 'FAMILY', 'PHOTOGRAPHY', 'MEDICAL', 'TOOLS', 'FINANCE', 'LIFESTYLE', 'BUSINESS'])],
                                x="Price", y="Category", hover_data=["App"],
                                title="App Pricing Trend Across Categories",
                                template="simple_white")
            ),
            html.P("Most apps are clustered around lower price ranges (0–10 dollars) across all categories. High-price novelty apps appear mainly in Lifestyle and Finance.")
        ])
    ], className="mb-4"),

    # Section: Free vs Paid Downloads
    dbc.Card([
        dbc.CardHeader("👅 Downloads: Free vs Paid Apps"),
        dbc.CardBody([
            dcc.Graph(
                figure=px.box(apps, x="Type", y="Installs", color="Type", log_y=True,
                              title="Number of Downloads: Free vs Paid Apps",
                              template="simple_white")
            ),
            html.P("Free apps dominate downloads. Paid apps have more modest and consistent install numbers.")
        ])
    ], className="mb-4"),

    # Top Apps by Reviews and Installs
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📊 Top 5 Apps by Reviews"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id="review-type-dropdown",
                        options=[
                            {"label": "🏆 Top 5 Free Apps by Reviews", "value": "Free"},
                            {"label": "💎 Top 5 Paid Apps by Reviews", "value": "Paid"},
                        ],
                        value="Free",
                        clearable=False,
                        className="mb-3"
                    ),
                    dcc.Graph(id="top-apps-by-reviews-graph"),
                    html.P(id="top-apps-description", className="mt-3")
                ])
            ])
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📈 Top 5 Apps by Installs"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id="install-type-dropdown",
                        options=[
                            {"label": "📅 Top 5 Free Apps by Installs", "value": "Free"},
                            {"label": "💰 Top 5 Paid Apps by Installs", "value": "Paid"},
                        ],
                        value="Free",
                        clearable=False,
                        className="mb-3"
                    ),
                    dcc.Graph(id="top-apps-by-installs-graph"),
                    html.P(id="top-installs-description", className="mt-3")
                ])
            ])
        ], md=6)
    ], className="mb-4"),


    # Category Engagement Metric
    dbc.Card([
        dbc.CardHeader("📚 Top 10 Categories by Engagement"),
        dbc.CardBody([
            dcc.Dropdown(
                id="category-engagement-dropdown",
                options=[
                    {"label": "🔥 Top Categories by Total Installs", "value": "Installs"},
                    {"label": "💬 Top Categories by Total Reviews", "value": "Reviews"},
                ],
                value="Installs",
                clearable=False,
                className="mb-3"
            ),
            dcc.Graph(id="category-engagement-graph"),
            html.P(id="category-engagement-description", className="mt-3")
        ])
    ], className="mb-4"),

    html.Hr(),
    html.P("In summary, the Google Play Store shows strong dominance of utility and entertainment categories. "
           "While most apps are free and small, quality is consistent across sizes and prices. User engagement is highest in "
           "communication, social, and game apps.", className="text-muted")
], fluid=True)


# Top 5 Apps by Reviews Callback
@callback(
    Output("top-apps-by-reviews-graph", "figure"),
    Output("top-apps-description", "children"),
    Input("review-type-dropdown", "value")
)
def update_reviews_chart(app_type):
    df = apps[apps["Type"] == app_type]
    if df.empty:
        return px.bar(title="No Data Available"), "No data available for this app type."

    filtered_df = df.sort_values(by="Reviews", ascending=False).head(5)
    fig = px.bar(
        filtered_df,
        x="App", y="Reviews", title=f"Top 5 {app_type} Apps by Reviews",
        hover_data=["Installs", "Category", "Price"] if app_type == "Paid" else ["Installs", "Category"],
        template="simple_white"
    )

    desc = (
        "Meta-owned apps like Facebook and WhatsApp dominate with massive review counts and installs, highlighting their global engagement."
        if app_type == "Free" else
        "Minecraft leads paid apps by a large margin in reviews, showing rare engagement for a premium app and strong brand loyalty."
    )
    return fig, desc

# Top 5 Apps by Installs Callback
@callback(
    Output("top-apps-by-installs-graph", "figure"),
    Output("top-installs-description", "children"),
    Input("install-type-dropdown", "value")
)
def update_installs_chart(app_type):
    df = apps[apps["Type"] == app_type]
    if df.empty:
        return px.bar(title="No Data Available"), "No data available for this app type."

    filtered_df = df.sort_values(by="Installs", ascending=False).head(5)
    fig = px.bar(
        filtered_df,
        x="App", y="Installs", title=f"Top 5 {app_type} Apps by Installs",
        text="Installs",
        template="simple_white"
    ).update_layout(showlegend=False)

    desc = (
        "Google and Meta apps lead with over 1 billion installs, often due to being pre-installed or offering core services."
        if app_type == "Free" else
        "Minecraft and Hitman Sniper dominate paid installs, proving users pay for recognizable, high-value content."
    )
    return fig, desc

# Category Engagement Callback
@callback(
    Output("category-engagement-graph", "figure"),
    Output("category-engagement-description", "children"),
    Input("category-engagement-dropdown", "value")
)
def update_category_engagement_plot(selected_metric):
    if selected_metric == "Installs":
        df = top_installs
        y_column = "Installs"
        title = "Top 10 Categories with Highest Total Installs"
        desc = "Game and Communication apps dominate in installs, showing mass appeal. Others like Tools and Productivity succeed with fewer but impactful apps."
    else:
        df = top_reviews
        y_column = "Reviews"
        title = "Top 10 Categories with Highest Total Reviews"
        desc = "Most downloaded categories also tend to receive the highest reviews."

    fig = px.bar(
        df,
        x="Category", y=y_column,
        title=title,
        labels={y_column: f"Total {y_column}"},
        template="simple_white"
    ).update_layout(xaxis_tickangle=-45, height=600)
    
    return fig, desc

# App Size vs Price Toggle Tab Callback
@callback(
    Output("size-price-graph", "figure"),
    Output("size-price-description", "children"),
    Input("size-price-tabs", "value")
)
def update_size_price_tab(selected_tab):
    if selected_tab == "size":
        df = apps.dropna(subset=["Size in MBs", "Rating"])
        if df.empty:
            return px.scatter(title="No Data Available"), "No data available for size vs. rating."

        fig = px.scatter(
            df,
            x="Size in MBs", y="Rating",
            hover_data=["App", "Category"],
            marginal_x="histogram", marginal_y="histogram",
            title="App Size vs. Rating with Histograms",
            template="simple_white"
        )
        desc = "App size has little correlation with ratings. Both small and large apps receive high ratings."
    else:
        df = apps[(apps["Type"] == "Paid") & (apps["Rating"].notna())]
        if df.empty:
            return px.scatter(title="No Data Available"), "No data available for paid app prices."

        fig = px.scatter(
            df,
            x="Price", y="Rating",
            hover_data=["App", "Category"],
            marginal_x="histogram", marginal_y="histogram",
            title="Price vs Rating for Paid Apps with Histograms",
            template="simple_white"
        )
        desc = "Most paid apps are under $10. Expensive apps receive mixed reviews—price does not guarantee quality."
    
    return fig, desc

