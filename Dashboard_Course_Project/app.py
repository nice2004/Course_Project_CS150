# -*- coding: utf-8 -*-
from assets import words
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
from Cleaning_data import df

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
    # data=[],  # Replace with df.to_dict('records') when ready
    page_size=10,
    style_table={"overflowX": "auto"},
    style_cell={"textAlign": "left", "padding": "6px"},
)

Occupation_dropdown = dcc.Dropdown(
    id='occupation-dropdown',
    options=[{'label', 'value'},
             {'label': 'University Student', 'value': 'university-student'},
             {'label': 'Salaried Worker', 'value': 'salaried-worker'},
             {'label': 'Retired', 'value': 'retired'},
             ],
    value='University Student',
    clearable=False,
    style={'width': '100%'}
)

Platform_dropdown = dcc.Dropdown(
    id='platform-dropdown',
    options=[{'label': 'Instagram', 'value': 'Instagram'},
             {'label': 'YouTube', 'value': 'YouTube'},
             {'label': 'Pinterest', 'value': 'Pinterest'},
             {'label': 'Twitter', 'value': 'Twitter'},
             {'label': 'Discord', 'value': 'Discord'},
             {'label': 'Reddit', 'value': 'Reddit'},
             {'label': 'Snapchat', 'value': 'Snapchat'},
             {'label': 'TikTok', 'value': 'TikTok'},
             {'label': 'Discord', 'value': 'Discord'}],
    value='Facebook',
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
        dbc.Col(dcc.Graph(id='social_chart', className='mb-2'), width=6),
        dbc.Col(dcc.Graph(id='productive_chart', className='pb-4'), width=6),
    ]),
    html.Hr(),
    html.H6(words.datasource_text, className='my-2')
])

# =====  Productivity Detector components

detector_text = dbc.Card(words.play_text, className='card-title')

Age = dbc.InputGroup(
    [
        dbc.InputGroupText("Select your age"),
        dcc.Dropdown(
            id="age",
            options=[{'label': str(i), 'value': i} for i in df['Age'].unique()],
            clearable=False,
            style={'width': '100%'}
        ),
    ],
    className="mb-3",
)

Gender = dbc.InputGroup([
    dbc.InputGroupText('Select your Gender'),
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

Relationship_status = dbc.InputGroup([
    dbc.InputGroupText('Select your status'),
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

Occupation_status = dbc.InputGroup([
    dbc.InputGroupText('Select your status'),
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

time_spent = dbc.InputGroup(
    [
        dbc.InputGroupText("Select time spent"),
        dcc.Dropdown(
            id="time_spent",
            options=[{'label': str(i), 'value': i} for i in df['Time Spent'].unique()],
            clearable=False,
            style={'width': '100%'}
        ),
    ],
    className="mb-3",
)

media_platforms = dbc.InputGroup(
    [
        dbc.InputGroupText("Select Platforms you use"),
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
                     {'label': 'YouTube', 'value': 'Youtube'}
                     ],
            # clearable=False,
            value=[],
            style={'width': '100%'}
        ),
    ],
    className="mb-3",
)
distraction_level = dcc.Slider(0, 5, 1, value=3, marks={i: str(i) for i in range(0, 6)}, id='distraction-slider')
concentration_level = dcc.Slider(0, 5, 1, value=3, marks={i: str(i) for i in range(0, 6)}, id='concentration-slider')

input_groups = html.Div(
    [Age, Gender, Relationship_status, Occupation_status, time_spent, media_platforms, distraction_level,
     concentration_level],
    className='mt-4')

productivity_feedback = html.Div(id='productivity-output', className='mt-3')

# ========= Dataset Tab components

dataset_card = dbc.Card([
    dbc.CardHeader('Social Media and Productivity Analysis Dataset'),
    html.Div(dataset_table),
],
    className='mt-4')

# ======== Build Tabs Components

tabs = dbc.Tabs([
    dbc.Tab(learn_card, tab_id='tab1', label='Learn'),
    dbc.Tab(graph_tab_content,
            tab_id='tab2',
            label='Graphic',
            className='pb-4',
            ),
    dbc.Tab([words.play_text, input_groups, productivity_feedback], tab_id='tab3', label='🧠 Productivity Detector')
],
    id='tabs',
    # active_tab='tab2',
    className='mt-2')

"""
==========================================================================
Helper functions
"""

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


@app.callback(
    Output('productivity-output', 'children'),
    Input('time_spent', 'value'),
    Input('distraction-slider', 'value'),
    Input('concentration-slider', 'value'),
    Input('media_platforms', 'value')
)
def detect_productivity(time, distraction, concentration, platforms):
    # Convert strings to numbers if needed
    try:
        time = float(time)
        distraction = float(distraction)
        concentration = float(concentration)
    except (TypeError, ValueError):
        return html.Div("⚠️ Please make sure all sliders are selected.", style={"color": "orange"})

    warning_thresholds = {
        "time": 5,
        "distraction": 7,
        "concentration": 4
    }

    if time > warning_thresholds["time"] and distraction > warning_thresholds["distraction"] and concentration < \
            warning_thresholds["concentration"]:
        return html.Div([
            html.H3("⚠️ Productivity Alert!", style={"color": "red"}),
            html.P("Your current patterns suggest high distraction and low focus. Try reducing screen time or taking "
                   "purposeful breaks.")
        ])
    elif time <= 3 and distraction <= 4 and concentration >= 6:
        return html.Div([
            html.H3("✅ You're Thriving!", style={"color": "green"}),
            html.P("Great job! Your social media habits seem balanced and productive. Keep it up!")
        ])
    else:
        return html.Div([
            html.H3("🟡 Mixed Signals", style={"color": "orange"}),
            html.P("Some aspects of your habits are okay, but there might be room to improve. Consider limiting time "
                   "on:"),
            html.Ul([html.Li(platform) for platform in platforms or []])
        ])


if __name__ == "__main__":
    app.run(debug=True)
