# -*- coding: utf-8 -*-
from assets import words
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
from Cleaning_data import df, df1
import plotly.express as px

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.FONT_AWESOME],
)

"""
==========================================================================
Tables and Dropdowns
"""

dataset_table = dash_table.DataTable(
    id="dataset-table",
    columns=[
        {"id": "Age", "name": "Age", "type": "numeric"},
        {"id": "Gender", "name": "Gender", "type": "text"},
        {"id": "Relationship Status", "name": "Relationship Status", "type": "text"},
        {"id": "Occupation Status", "name": "Occupation Status", "type": "text"},
        {"id": "Students", "name": "Students", "type": "text"},
        {"id": "use_social_media", "name": "use_social_media", "type": "text"},
        {"id": "Time Spent", "name": "Time Spent", "type": "text"},
        {"id": "Use Social Media without Purpose", "name": "Use Social Media without Purpose", "type": "numeric"},
        {"id": "Often you get distracted by social media", "name": "Often you get distracted by social media",
         "type": "numeric"},
        {"id": "11. Do you feel restless if you haven't used Social media in a while?",
         "name": "11. Do you feel restless if you haven't used Social media in a while?", "type": "numeric"},
        {"id": "Distraction level", "name": "Distraction level", "type": "numeric"},
        {"id": "Worries Level", "name": "Worries Level", "type": "numeric"},
        {"id": "Concentration level", "name": "Concentration level", "type": "numeric"},
        {"id": "Comparison Level", "name": "Comparison Level", "type": "numeric"},
        {"id": "Comparison Feeling", "name": "Comparison Feeling", "type": "numeric"},
        {"id": "Validation", "name": "Validation", "type": "numeric"},
        {"id": "Depression level", "name": "Depression level", "type": "numeric"},
        {"id": "Fluctuation of Interest in daily activities", "name": "Fluctuation of Interest in daily activities",
         "type": "numeric"},
        {"id": "Sleep Issues level", "name": "Sleep Issues level", "type": "numeric"},
        {"id": "Discord", "name": "Discord", "type": "numeric"},
        {"id": "Facebook", "name": "Facebook", "type": "numeric"},
        {"id": "Instagram", "name": "Instagram", "type": "numeric"},
        {"id": "Pinterest", "name": "Pinterest", "type": "numeric"},
        {"id": "Reddit", "name": "Reddit", "type": "numeric"},
        {"id": "Snapchat", "name": "Snapchat", "type": "numeric"},
        {"id": "Tiktok", "name": "TikTok", "type": "numeric"},
        {"id": "Twitter", "name": "Twitter", "type": "numeric"},
        {"id": "Youtube", "name": "Youtube", "type": "numeric"},
    ],
    data=df.to_dict('records'),
    page_size=10,
    style_table={"overflowX": "auto"},
    style_cell={"textAlign": "left", "padding": "6px"},
)

dataset2_table = dash_table.DataTable(
    id="dataset2-table",
    columns=[
        {"id": "user_id", "name": "user_id", "type": "numeric"},
        {"id": "post_type", "name": "post_type", "type": "text"},
        {"id": "post_length", "name": "post_length", "type": "numeric"},
        {"id": "likes", "name": "likes", "type": "numeric"},
        {"id": "comments", "name": "comments", "type": "numeric"},
        {"id": "shares", "name": "shares", "type": "numeric"},
        {"id": "engagement_rate", "name": "engagement_rate", "type": "numeric"},
        {"id": "user_followers", "name": "user_followers", "type": "numeric"},
        {"id": "post_category", "name": "post_category", "type": "text"},
        {"id": "post_hour", "name": "post_hour", "type": "numeric"},
        {"id": "is_weekend", "name": "is_weekend", "type": "numeric"},
        {"id": "user_verified", "name": "user_verified", "type": "numeric"},
        {"id": "spam_flag", "name": "spam_flag", "type": "numeric"},
    ],
    data=df1.to_dict('records'),
    page_size=10,
    style_table={"overflowX": "auto"},
    style_cell={"textAlign": "left", "padding": "6px"},
)

Occupation_dropdown = dcc.Dropdown(
    id='occupation-dropdown',
    options=[{'label': 'All Occupations', 'value': 'all'},
             {'label': 'University Student', 'value': 'University Student'},
             {'label': 'Salaried Worker', 'value': 'Salaried Worker'},
             {'label': 'Retired', 'value': 'Retired'},
             ],
    value='all',
    clearable=False,
    style={'width': '100%'}
)

Platform_dropdown = dcc.Dropdown(
    id='platform-dropdown',
    options=[{'label': 'All Platforms', 'value': 'all'},
             {'label': 'Instagram', 'value': 'Instagram'},
             {'label': 'Youtube', 'value': 'Youtube'},
             {'label': 'Pinterest', 'value': 'Pinterest'},
             {'label': 'Twitter', 'value': 'Twitter'},
             {'label': 'Discord', 'value': 'Discord'},
             {'label': 'Reddit', 'value': 'Reddit'},
             {'label': 'Snapchat', 'value': 'Snapchat'},
             {'label': 'TikTok', 'value': 'TikTok'},
             {'label': 'Discord', 'value': 'Discord'}],
    value='all',
    clearable=False,
    style={'width': '100%'}
)

"""
==========================================================================
Figures
"""


def empty_bar_chart():
    fig = go.Figure()
    fig.update_layout(
        title="No data available",
        height=400,
        template="plotly_white"
    )
    fig.add_annotation(
        text="Select valid filter options to display data",
        showarrow=False,
        font=dict(size=16)
    )
    return fig


def empty_line_chart():
    fig = go.Figure()
    fig.update_layout(
        title="No data available",
        height=400,
        template="plotly_white"
    )
    fig.add_annotation(
        text="Select valid filter options to display data",
        showarrow=False,
        font=dict(size=16)
    )
    return fig


"""
==========================================================================
Make Tabs
"""

# =======Learn tab components
learn_card = dbc.Card(
    [
        dbc.CardHeader("An Introduction to Asset Allocation"),
        dbc.CardBody(words.learn_text),
    ],
    className="mt-4",
)

# ======= Graph tab components

graph_text = dbc.Card(words.asset_allocation_text, className='card-title')
graph_tab_content = html.Div([
    graph_text,
    dbc.Row([
        dbc.Col([
            html.Label('Select Post Category', className='form-label'),
            dcc.Dropdown(
                id='post-category-dropdown',
                options=[{'label': category, 'value': category} for category in df1['post_category'].unique()],
                value=df1['post_category'].unique()[0],
                clearable=False,
                style={'width': '100%'}
            ),
            dcc.Graph(id='post-type-engagement-graph', className='mt-3')
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            html.H6("Filter by Occupation:"),
            Occupation_dropdown,
        ], width=6),
        dbc.Col([
            html.H6("Filter by Platform:"),
            Platform_dropdown,
        ], width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='social_chart', className='mb-2'), width=6),
        dbc.Col(dcc.Graph(id='productivity-chart', className='pb-4'), width=6),
    ]),

    html.Hr(),
    html.H6(words.datasource_text, className='my-2')
])

# =====  Productivity Detector components

detector_text = dbc.Card(words.play_text, className='card-title')

Age = html.Div(
    [
        html.Label("Select your age", className='form-label'),
        dcc.Dropdown(
            id="age",
            options=[{'label': str(i), 'value': i} for i in df['Age'].unique()],
            clearable=False,
            style={'width': '100%'}
        ),
    ],
    className="mb-3",
)

Gender = html.Div([
    html.Label('Select your Gender', className='form-label'),
    dcc.RadioItems(
        id='gender',
        options=[{'label': 'Female', 'value': 'Female'},
                 {'label': 'Male', 'value': 'Male'},
                 {'label': 'Other', 'value': 'Other'}],
        # clearable=False,
        style={'width': '100%'}
    )
],
    className="mb-3"
)

Relationship_status = html.Div([
    html.Label('Select your status', className='form-label'),
    dcc.Dropdown(
        id='relationship-status',
        options=[{'label': 'Single', 'value': 'Single'},
                 {'label': 'Married', 'value': 'Married'},
                 {'label': 'In a relationship', 'value': 'Other'}],
        clearable=False,
        style={'width': '100%'}
    )
],
    className="mb-3"
)

Occupation_status = html.Div([
    html.Label('Select your status', className='form-label'),
    dcc.RadioItems(
        id='occupation-status',
        options=[{'label': 'University Student', 'value': 'university_student'},
                 {'label': 'Salaried Worker', 'value': 'salaried_worker'},
                 {'label': 'Retired', 'value': 'Retired'}],
        # clearable=False,
        style={'width': '100%'}
    )
],
    className="mb-3"
)

time_spent = html.Div(
    [
        html.Label("Select time spent", className='form-label'),
        dcc.Dropdown(
            id="time_spent",
            options=[{'label': str(i), 'value': i} for i in df['Time Spent'].unique()],
            clearable=False,
            style={'width': '100%'}
        ),
    ],
    className="mb-3",
)

media_platforms = html.Div(
    [
        html.Label("Select Platforms you use", className='form-label'),
        dcc.Checklist(
            id="media_platforms",
            options=[{'label': 'Discord', 'value': 'Discord'},
                     {'label': 'Facebook', 'value': 'Facebook'},
                     {'label': 'Instagram', 'value': 'Instagram'},
                     {'label': 'Pinterest', 'value': 'Pinterest'},
                     {'label': 'Reddit', 'value': 'Reddit'},
                     {'label': 'Snapchat', 'value': 'Snapchat'},
                     {'label': 'TikTok', 'value': 'Tiktok'},
                     {'label': 'Twitter', 'value': 'Twitter'},
                     {'label': 'Youtube', 'value': 'Youtube'}
                     ],
            value=[],
            style={'width': '100%'}
        ),
    ],
    className="mb-3",
)

distraction_level = html.Div([
    html.Label('Select your distraction level', className='form-label'),
    dcc.Slider(0, 5, 1, value=3, marks={i: str(i) for i in range(0, 6)}, id='distraction-slider')
],
    className="mb-4"
)

concentration_level = html.Div([
    html.Label('Select your concentration level', className='form-label'),
    dcc.Slider(0, 5, 1, value=3, marks={i: str(i) for i in range(0, 6)}, id='concentration-slider')
],
    className="mb-4"
)

button = dbc.Button(
    'Analyze your productivity',
    id='button',
    color='primary',
    className='mt-3'
)

# input_groups = html.Div(
#     [Age, Gender, Relationship_status, Occupation_status, time_spent, media_platforms, distraction_level,
#      concentration_level],
#     className='mt-4')

productivity_feedback = html.Div(id='productivity-output', className='mt-3')

detector_tab = html.Div([
    words.play_text,
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Your Information"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([Age, Gender], width=12, md=6),
                        dbc.Col([Relationship_status, Occupation_status], width=12, md=6),
                    ]),
                    dbc.Row([
                        dbc.Col([time_spent], width=12),
                    ]),
                    dbc.Row([
                        dbc.Col([media_platforms], width=12),
                    ]),
                    dbc.Row([
                        dbc.Col([distraction_level], width=12, md=6),
                    ]),
                    dbc.Row([
                        dbc.Col([concentration_level], width=12, md=6),
                    ]),
                    dbc.Button("Analyze Your Productivity", id="button", color="primary", className="mt-3"),
                ]),
            ]),
        ], width=12, lg=8),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Results"),
                dbc.CardBody([
                    productivity_feedback
                ]),
            ], className="h-100"),
        ], width=12, lg=4),
    ])
])

# ========= Dataset Tab components

dataset_tab = html.Div([
    dbc.Card([
        dbc.CardHeader(html.H5("Social Media and Productivity Datasets")),
        dbc.CardBody([
            html.Div([
                html.H6("Search and Filter:"),
                dbc.Row([
                    dbc.Col(dbc.Input(id="search-input", placeholder="Type to search...", type="text"), width=12, md=6),
                ], className="mb-3"),
                dataset_table,
                dataset2_table
            ]),
        ]),
    ]),
])

# ======== Build Tabs Components

tabs = dbc.Tabs([
    dbc.Tab(learn_card, tab_id='tab1', label='Learn'),
    dbc.Tab(graph_tab_content,
            tab_id='tab2',
            label='Graphic',
            className='pb-4',
            ),

    dbc.Tab(detector_tab, tab_id='tab3',
            label='🧠 Productivity Detector'),
    dbc.Tab(dataset_tab, tab_id='tab4', label='Dataset', className='pb-4')
],

    id='tabs',
    # active_tab='tab2',
    className='mt-2')

"""
==========================================================================
Helper functions
"""


def create_productivity_chart(data, occupation=None, platform=None):
    filtered_df = data.copy()

    # Filter by occupation if provided and not 'all'
    if occupation and occupation != 'all':
        filtered_df = filtered_df[filtered_df['Occupation Status'] == occupation]

    # Filter by platform if provided and not 'all'
    if platform and platform != 'all':
        # Print to debug what data is available for this platform
        print(f"Filtering for {platform} users")
        print(f"Count of {platform} users: {filtered_df[platform].sum()}")

        # Make sure we're using the correct column name
        if platform in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[platform] == 1]
            print(f"After filtering: {len(filtered_df)} rows")
            print(f"Time ranges available: {filtered_df['Time Spent'].unique()}")
        else:
            print(f"Warning: Platform column '{platform}' not found in dataframe")

    # Check if we have data after filtering
    if len(filtered_df) == 0:
        print("No data available after filtering")
        return empty_line_chart()

    # Group by time spent
    time_groups = filtered_df.groupby('Time Spent')
    productivity_data = {'Time Spent': [], 'Concentration Score': [], 'Distraction Score': []}

    # Print how many groups we have
    print(f"Number of time groups: {len(time_groups)}")

    for time, group in time_groups:
        productivity_data['Time Spent'].append(time)
        productivity_data['Concentration Score'].append(5 - group['Concentration level'].mean())
        productivity_data['Distraction Score'].append(group['Distraction level'].mean())

    # Convert to DataFrame for plotting
    df_prod = pd.DataFrame(productivity_data)

    # Define the correct order of time ranges
    time_order = ["Less than an Hour",
                  "Between 1 and 2 hours",
                  "Between 2 and 3 hours",
                  "Between 3 and 4 hours",
                  "Between 4 and 5 hours",
                  "More than 5 hours"]

    # Make sure all time ranges are represented
    for time in time_order:
        if time not in df_prod['Time Spent'].values:
            print(f"Adding missing time range: {time}")
            # Add row with NaN values for metrics
            new_row = pd.DataFrame({'Time Spent': [time], 'Concentration Score': [None], 'Distraction Score': [None]})
            df_prod = pd.concat([df_prod, new_row], ignore_index=True)

    # Order by the defined sequence
    df_prod['Time Spent'] = pd.Categorical(df_prod['Time Spent'], categories=time_order, ordered=True)
    df_prod.sort_values('Time Spent', inplace=True)

    # Create the plot
    fig = px.line(
        df_prod,
        x='Time Spent',
        y=['Concentration Score', 'Distraction Score'],
        markers=True,
        line_shape='spline',
        color_discrete_sequence=['#2C6E49', '#D62828'],
    )

    # Set plot title
    title = 'Productivity Metrics by Social Media Usage'
    if occupation and occupation != 'all':
        title += f' - {occupation}'
    if platform and platform != 'all':
        title += f' - {platform} Users'

    fig.update_layout(
        title=title,
        height=400,
        template='plotly_white',
        legend_title='Metrics',
        xaxis_title='Daily Time Spent on Social Media',
        yaxis_title='Average Score (0-5)',
        yaxis=dict(range=[0, 5]),
        margin=dict(l=40, r=20, t=60, b=40),
    )

    return fig

"""
===========================================================================
Main Layout
"""

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H4(
                'Social Media and Productivity Analysis',
                className='bg-primary p-2 mb-2 text-center text-white'
            )
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.H5(
                'Nice Teta Hirwa - CS150 - Professor Mike Ryu',
                className='bg-primary p-2 mb-2 text-center text-white'
            )
        )
    ], style={'marginBottom': '10px'}),

    dbc.Row([
        dbc.Col(tabs, width=12, className='mt-4 border'),
    ], className='ms-1'),
    dbc.Row(
        dbc.Col(html.H6(words.footer))
    )

], fluid=True)

"""
==========================================================================
Callbacks
"""


@app.callback(Output('post-type-engagement-graph', 'figure'),
              Input('post-category-dropdown', 'value'))
def update_post_graph(selected_category):
    filtered_df = df1[df1['post_category'] == selected_category]

    avg_engagement = filtered_df.groupby('post_type')['engagement_rate'].mean().reset_index()
    fig = go.Figure(
        data=[
            go.Bar(
                x=avg_engagement['post_type'],
                y=avg_engagement['engagement_rate'],
                marker_color='lightskyblue'
            )
        ]
    )
    # Set Y-axis range with some padding, assuming engagement_rate typically ranges between 0 and 1
    y_min = avg_engagement['engagement_rate'].min() - 0.05  # adding a bit of padding
    y_max = avg_engagement['engagement_rate'].max() + 0.05  # adding a bit of padding

    fig.update_layout(
        title=f"Average Engagement Rate by Post Type ({selected_category})",
        xaxis_title="Post Type",
        yaxis_title="Engagement Rate",
        yaxis=dict(range=[y_min, y_max]),  # Apply Y-axis scaling here
        template="plotly_white",
        height=500
    )

    return fig


@app.callback(Output('productivity-chart', 'figure'),
              [Input('occupation-dropdown', 'value'),
               Input('platform-dropdown', 'value')])
def update_charts(occupation, platform):
    filtered_df = df.copy()

    if occupation != 'all':
        filtered_df = filtered_df[filtered_df['Occupation Status'] == occupation]
        print(f"Filtered Data after occupation: {filtered_df.shape}")
    productivity_fig = create_productivity_chart(
        filtered_df,
        None if occupation == 'all' else occupation,
        None if platform == 'all' else platform
    )

    # # Find most used platform
    # platform_columns = ['Facebook', 'Instagram', 'Youtube', 'Twitter', 'Tiktok', 'Reddit', 'Pinterest', 'Snapchat',
    #                     'Discord']
    # platform_usage = {col: filtered_df[col].sum() for col in platform_columns}
    # most_used = max(platform_usage.items(), key=lambda x: x[1])[0]

    return productivity_fig


if __name__ == "__main__":
    app.run(debug=True)
