import dash.react import Dash

app = Dash('my app')

from dash_components import h1, PlotlyGraph
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=spc_common,count(tree_id)' +\
        '&$group=spc_common').replace(' ', '%20')
soql_trees = pd.read_json(soql_url)
unique_trees = soql_trees['spc_common']

app.layout = h1('Arborist App'),
html.Div([
    dcc.Dropdown(id='Borough Selection',
                 options=[
                 {'label': 'Brooklyn', 'value': 'Brooklyn'},
                 {'label': 'Bronx', 'value': 'Bronx'},
                 {'label': 'Manhattan', 'value': 'Manhattan'},
                 {'label': 'Queens', 'value': 'Queens'},
                 {'label': 'Staten Island', 'value': 'Staten Island'},
                 ], value = 'brooklyn'),
]),
html.Div([
    dcc.Dropdown(id='Species Selection',
                 options=[
                 {'label': unique_trees[i], 'value': unique_trees[i]} for i in range(len(unique_trees))
                 ], value = unique_trees[0]),
]),

@app.react('graph1', ['Borough Selection'])
def update_graphs(borough):
    boro = borough.value
    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=spc_common,health,count(tree_id)' +\
        '&$where=boroname=\'{}\'' +\
        '&$group=spc_common,health').format(boro).replace(' ', '%20')
    df = pd.read_json(soql_url)
    trace1 = go.Bar(x=df.loc[df['health']=='Fair', 'spc_common'], y=df['count_tree_id)'])
    trace2 = go.Bar(x=df.loc[df['health']=='Poor', 'spc_common'], y=df['count_tree_id)'])
    trace3 = go.Bar(x=df.loc[df['health']=='Good', 'spc_common'], y=df['count_tree_id)'])

    return {
    'data': [trace1, trace2, trace3, trace4],
    'layout':
    go.Layout(
        title='Tree Health in {}'.format(boro),
        barmode='stack')
    }

if __name__ == '__main__':
    app.server.run(debug = True)
