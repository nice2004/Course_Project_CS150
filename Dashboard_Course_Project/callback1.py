import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# This code would normally go in a separate file for your ML model
def build_productivity_model(df):
    """Build a machine learning model to predict productivity scores"""

    # Create a productivity score based on concentration and distraction levels
    # Higher concentration is good, higher distraction is bad
    df['productivity_score'] = (5 - df['Distraction level']) + df['Concentration level']
    # Normalize to 0-100 scale
    df['productivity_score'] = (df['productivity_score'] / 10) * 100

    # Define features
    categorical_features = ['Gender', 'Relationship Status', 'Occupation Status', 'Time Spent']
    numerical_features = ['Age', 'Use Social Media without Purpose',
                          'Often you get distracted by social media',
                          'Distraction level', 'Concentration level', 'Sleep Issues level']

    platform_features = ['Discord', 'Facebook', 'Instagram', 'Pinterest',
                         'Reddit', 'Snapchat', 'Tiktok', 'Twitter', 'Youtube']

    # Combine all features
    all_features = categorical_features + numerical_features + platform_features

    # Create feature transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough'
    )

    # Create pipeline with preprocessor and model
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Prepare data
    X = df[all_features]
    y = df['productivity_score']

    # Train the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)

    # Evaluate the model
    y_pred = pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Model MSE: {mse}")

    return pipeline


# Function to generate insights based on productivity score
def generate_productivity_insights(score, user_inputs):
    insights = []

    # General score assessment
    if score >= 80:
        assessment = "Excellent productivity potential"
        color = "success"
    elif score >= 60:
        assessment = "Good productivity potential"
        color = "info"
    elif score >= 40:
        assessment = "Moderate productivity potential"
        color = "warning"
    else:
        assessment = "Productivity challenges identified"
        color = "danger"

    # Specific insights based on inputs
    if user_inputs.get('purpose_level', 0) > 3:
        insights.append("Try setting clear goals before using social media")

    if user_inputs.get('sleep_level', 0) > 3:
        insights.append("Improving sleep quality may boost your productivity")

    if user_inputs.get('distraction_level', 0) > 3:
        insights.append("Consider using focus apps or website blockers")

    if user_inputs.get('concentration_level', 0) < 3:
        insights.append("Try the Pomodoro technique (25 min work, 5 min break)")

    # Platform-specific insights
    platforms = user_inputs.get('media_platforms', [])
    if 'Instagram' in platforms and 'Tiktok' in platforms:
        insights.append("Visual platforms like Instagram and TikTok can be particularly distracting")

    if len(platforms) > 4:
        insights.append("Using fewer social platforms may help focus your attention")

    time_spent = user_inputs.get('time_spent', '')
    if "More than 5 hours" in time_spent or "Between 4 and 5 hours" in time_spent:
        insights.append("Consider setting daily time limits for social media use")

    return assessment, color, insights


# Create a productivity meter visualization
def create_productivity_meter(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Productivity Score"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': get_color_for_score(score)},
            'steps': [
                {'range': [0, 25], 'color': "#ff0000"},
                {'range': [25, 50], 'color': "#ffa500"},
                {'range': [50, 75], 'color': "#ffff00"},
                {'range': [75, 100], 'color': "#008000"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=30, b=20)
    )

    return fig


def get_color_for_score(score):
    if score >= 75:
        return "#008000"  # Green
    elif score >= 50:
        return "#ffff00"  # Yellow
    elif score >= 25:
        return "#ffa500"  # Orange
    else:
        return "#ff0000"  # Red


# Function to register callbacks
def register_productivity_callbacks(app, df):
    # Build our model once at startup
    model = build_productivity_model(df)

    @app.callback(
        Output('productivity-output', 'children'),
        [Input('button', 'n_clicks')],
        [Input('age', 'value'),
         Input('gender', 'value'),
         Input('relationship-status', 'value'),
         Input('occupation-status', 'value'),
         Input('time_spent', 'value'),
         Input('media_platforms', 'value'),
         Input('distraction-slider', 'value'),
         Input('concentration-slider', 'value'),
         Input('sleep_level', 'value'),
         Input('purpose_level', 'value')]
    )
    def update_productivity_output(n_clicks, age, gender, relationship_status,
                                   occupation_status, time_spent, media_platforms,
                                   distraction_level, concentration_level,
                                   sleep_level, purpose_level):
        if n_clicks is None:
            # Initial state - no prediction yet
            return html.Div([
                html.H5("Enter your information and click 'Analyze Your Productivity'",
                        className="text-center text-muted my-4")
            ])

        # Map occupation_status to the values in the dataset
        if occupation_status == "university_student":
            occupation_status = "University Student"
        elif occupation_status == "salaried_worker":
            occupation_status = "Salaried Worker"

        # Map relationship_status
        if relationship_status == "Other":
            relationship_status = "In a relationship"

        # Create input data for prediction
        input_data = {
            'Age': age,
            'Gender': gender,
            'Relationship Status': relationship_status,
            'Occupation Status': occupation_status,
            'Time Spent': time_spent,
            'Use Social Media without Purpose': purpose_level,
            'Often you get distracted by social media': distraction_level,
            'Distraction level': distraction_level,
            'Concentration level': concentration_level,
            'Sleep Issues level': sleep_level,
            'Discord': 1 if 'Discord' in media_platforms else 0,
            'Facebook': 1 if 'Facebook' in media_platforms else 0,
            'Instagram': 1 if 'Instagram' in media_platforms else 0,
            'Pinterest': 1 if 'Pinterest' in media_platforms else 0,
            'Reddit': 1 if 'Reddit' in media_platforms else 0,
            'Snapchat': 1 if 'Snapchat' in media_platforms else 0,
            'Tiktok': 1 if 'TikTok' in media_platforms else 0,
            'Twitter': 1 if 'Twitter' in media_platforms else 0,
            'Youtube': 1 if 'Youtube' in media_platforms else 0
        }

        # Create dataframe from input_data
        input_df = pd.DataFrame([input_data])

        # Make prediction
        productivity_score = model.predict(input_df)[0]

        # Round the score to an integer
        productivity_score = round(productivity_score)

        # Ensure score is within 0-100 range
        productivity_score = max(0, min(100, productivity_score))

        # Get insights
        user_inputs = {
            'purpose_level': purpose_level,
            'sleep_level': sleep_level,
            'distraction_level': distraction_level,
            'concentration_level': concentration_level,
            'media_platforms': media_platforms,
            'time_spent': time_spent
        }
        assessment, color, insights = generate_productivity_insights(productivity_score, user_inputs)

        # Create the visualization and results
        return html.Div([
            html.Div([
                dcc.Graph(figure=create_productivity_meter(productivity_score)),
            ]),
            html.H4(assessment, className=f"text-{color} text-center mt-3"),
            html.Hr(),
            html.H5("Personalized Insights:", className="mt-3"),
            html.Ul([html.Li(insight) for insight in insights], className="mt-2"),
            html.Hr(),
            html.P([
                "Social media usage pattern analysis: ",
                html.Strong(f"{len(media_platforms)} platforms"),
                ", with ",
                html.Strong(f"{time_spent}"),
                " daily usage."
            ], className="mt-3")
        ])