import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import dash_table
import tab1
from dash.dependencies import Input, Output, State


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dftsa=pd.read_csv('tsa_claims_ujian.csv')

    
app.layout = html.Div(children = [
    html.H1('Ujian Modul 2 Dashboard TSA'),
    html.P('Created by : Lazuardi Yusril Ihza'),
        dcc.Tabs(value = 'tabs',id = 'tabs-1',children= [
            tab1.table1,tab1.table2,tab1.table3,tab1.table4],content_style={
            'fontFamily' : 'Arial',
            'borderBottom' : '1px solid #d6d6d6',
            'borderLeft' : '1px solid #d6d6d6',
            'borderRight' : '1px solid #d6d6d6',
            'padding' : '44px'
        })
        
],style={
        'maxWidth' :'1000px',
        'margin' :'0 auto'
})

@app.callback(
    Output(component_id = 'contoh-graph-bar',component_property = 'figure'),
    [Input(component_id = 'x-axis1', component_property = 'value'),
    Input(component_id = 'x-axis2', component_property = 'value')]
)
def create_graph(y1,y2,x):
    figure={
                'data':[
                    {'x':dftsa[x],'y':dftsa[y1],'type':'bar','name':y1},
                    {'x':dftsa[x],'y':dftsa[y2],'type':'bar','name':y2},
                ],
                'layout': {'title': 'Bar Chart'}
                }
    return figure

@app.callback(
    Output(component_id = 'contoh-graph-pie',component_property = 'figure'),
    [Input(component_id = 'pie', component_property = 'value')]
)
def create_pie(x):
    figure={
                'data':[
                        go.Pie(labels = ['Generation{}'.format(i) for i in list(dftsa['Claim Type'].unique())],
                                        values = [dftsa.groupby('Claim Ttype').mean()[x][i] for i in list(dftsa['Claim Type'].unique())],
                                        sort = False)
                        ],
                        'layout': {'title': 'Mean Pie Chart'}
                }
    return figure


@app.callback(
    [Output(component_id = 'table',component_property = 'data'),
    Output(component_id='table',component_property='page_size')],
    [Input(component_id = 'search', component_property = 'n_clicks')],
    [State(component_id='claim_type',component_property='value'),
    State(component_id='num',component_property='value')]
)
def create_table(n_clicks,x1,x2):
        
    if x1 == 'All':
        data = dftsa.to_dict('records')
    else:
        data = dftsa[dftsa['Claim Site'] == x1].to_dict('records')
    page_size = x2
    return data, page_size


if __name__ == '__main__':
    app.run_server(debug=True)