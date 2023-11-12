from pymongo import MongoClient
from collections import Counter
from dash import dcc, html
import dash
from dash.dependencies import Input, Output
import plotly.express as px

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['users_profiles']
collection = db['user_collection']

# Aggregate data
pipeline = [
    {
        "$group": {
            "_id": "$nationality",
            "user_count": {"$sum": 1},
            "average_age": {"$avg": "$age"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "nationality": "$_id",
            "user_count": 1,
            "average_age": {"$round": ["$average_age", 2]}
        }
    }
]

nationality_stats = list(collection.aggregate(pipeline))

# Find the most common email domains
email_domains = Counter(filter(lambda domain: domain, (user.get("domain_name", "") for user in collection.find())))
most_common_domain = email_domains.most_common(1)

# Dash setup
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(children=[
    html.H1(children='User Data Visualization'),

    dcc.Graph(
        id='nationality-bar-chart',
        figure=px.bar(nationality_stats, x='nationality', y='user_count', title='Number of Users by Nationality')
    ),

    dcc.Graph(
        id='average-age-pie-chart',
        figure=px.pie(nationality_stats, values='user_count', names='nationality', title='Average Age of Users by Nationality')
    ),

    dcc.Graph(
        id='most-common-domain-pie-chart',
        figure=px.pie(labels=[most_common_domain[0][0], 'Others'],
                      values=[most_common_domain[0][1], sum(email_domains.values()) - most_common_domain[0][1]],
                      title='Most Common Email Domains')
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
