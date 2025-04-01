import dash
from dash import dcc, html, callback, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

df = pd.DataFrame({
    "Winner" : ["Uruguay", "Italy", "Italy", "Uruguay", "Germany", "Brazil", "Brazil", "Great Britain", "Brazil", "Germany", "Argentina", "Italy", "Argentina", "Germany", "Brazil", "France", "Brazil", "Italy", "Spain", "Germany", "France", "Argentina" ], 
    "Times Won" : [2,4,4,2,4,5,5,1,5,4,3,4,3,4,5,2,5,4,1,4,2,3],
    "Runner up": ["Argentina", "Czech Republic", "Hungary", "Brazil", "Hungary", "Sweden", "Czech Republic", "Germany", "Italy", "Netherlands", "Netherlands", "Germany", "Germany", "Argentina", "Italy", "Brazil", "Germany", "France", "Netherlands", "Argentina", "Croatia", "France"],
    "Year" : [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022]
})

app = dash.Dash()

app.layout = html.Div([
    html.H1("FIFA World Cup Winners"),
        dcc.Dropdown(['Overview', 'Check by year', 'Check how many times each country has won'], placeholder="Select option (ex. Overview)", id='dropdown-selection'),
        html.Div([
            dcc.Dropdown(df["Winner"].unique(), placeholder="Select Country", id='country-selection'),
        ],style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(df["Year"], placeholder="Select Year", id='dropdown-years')
        ],style={'width': '50%', 'display': 'inline-block'}),
    dcc.Graph(id = 'graph')
])

@callback(
    Output('graph', 'figure'),
    Input('dropdown-selection', 'value'),
    Input("dropdown-years", 'value'),
    Input('country-selection', 'value')
)

def update_graph(value, year, country):
    if value == "Check by year":
        if year:
            row = df.loc[df["Year"] == year]
        else:
            row = df.loc[df["Year"] == 2022]
        fig = px.choropleth(
            row,
            locations = "Winner",
            locationmode="country names",
            color="Winner",
            color_discrete_map={"Winner": "green", "Runner up":"blue"},
            scope = "world",
        )
        fig.update_traces(name="Winner", legendgroup="group1", showlegend=True)
        fig2 = px.choropleth(
            row,
            locations = "Runner up",
            locationmode="country names",
            scope = "world",
        )
        fig2.update_traces(name="Runner up", legendgroup="group2", showlegend=True)
        fig.add_trace(fig2.data[0])
        fig.update_layout(legend_title_text='Finals Participants')
    elif value == "Check how many times each country has won":
        if country:
            temp = df.loc[df["Winner"] == country]
        else:
            temp = df.loc[df["Winner"] == "Italy"]
        fig = px.choropleth(
            temp,
            locations = "Winner",
            locationmode="country names",
            color = "Winner",
            scope = "world",
        )
    else:
        fig = px.choropleth(
            df,
            locations = "Winner",
            locationmode="country names",
            color = "Winner",
            color_continuous_scale = "Viridis",
            hover_data={"Times Won":True},
            scope = "world",
            #title = "FIFA World Cup Winners",
        )
        fig.update_layout(legend_title_text='Winners over the years')
    fig.update_layout(width=1100, height=522)
    fig.update_geos(showcountries=True, showcoastlines=False, showland=True, fitbounds="geojson")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

app.run(debug=True)