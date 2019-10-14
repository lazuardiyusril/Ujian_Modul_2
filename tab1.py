import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dftsa=pd.read_csv('tsa_claims_ujian.csv')
def all_claim():
    a = [{'label' : i, 'value' : i} for i in dftsa['Claim Site'].unique()]
    a.append({'label' : 'All', 'value' : 'All'})
    return a

table1 =  dcc.Tab(label = 'DataFrame Table',value='tab-satu', children =[
                html.Div(children =[
                html.Br(),
                html.P('Claim Site :'),
                    dcc.Dropdown(id='claim_site',
                        options=all_claim(),
                        value='All')
                    ],className='col-3'),
                html.Div(children =[
                html.P('Max Rows : '),
                    dcc.Input(
                        id='num',
                        type='number',
                        value = 10,
                        ),                
                    ],className = 'col-3'),
                html.Br(),
                html.Div(html.Button('search', id='search'), className = 'col-3'),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in dftsa.columns],
                data=dftsa.to_dict('records'),
                page_action='native',
                page_current=0,
                page_size=15,
                )])


table2=dcc.Tab(label = 'Bar Chart',value='tab-dua', children =[
                    html.Div(children =[
                    html.Div(children =[
                    html.P('Y1 :'),
                    dcc.Dropdown(id='y-axis1',
                        options=[{'label' : i,'value' : i}for i in dftsa.select_dtypes('number').columns],
                        value='Claim Amount')
                    ],className='col-3'),
                    html.Div(children =[
                    html.P('Y2 : '),
                    dcc.Dropdown(id='y-axis2',
                        options=[{'label' : i,'value' : i}for i in dftsa.select_dtypes('number').columns],
                        value='Close Amount')
                    ],className='col-3'),
                    html.Div(children =[
                    html.P('X :'),
                    dcc.Dropdown(id='x-axis1',
                        options=['Claim Type','Claim Site', 'Disposition'],
                        value='Claim Type')
                    ],className='col-3')
                    ],className='row'),
                    dcc.Graph(
                    id='contoh-graph-bar',
                    figure={
                        'data':[
                            {'x':dftsa['Claim Type'],'y':dftsa['Claim Amount'],'type':'bar','name':'Claim Amount'},
                            {'x':dftsa['Claim Type'],'y':dftsa['Close Amount'],'type':'bar','name':'Close Amount'}
                        ],
                        'layout': {'title': 'Bar Chart'}
                        }
                        ,),
                    ])

table3 = dcc.Tab(label = 'Scatter Chart', value='tab-tiga',children =[
                    dcc.Graph(
                    id = 'graph.scatter',
                    figure = {
                        'data':[
                        go.Scatter( 
                            x=dftsa['Claim Amount'],
                            y=dftsa['Close Amount'],
                            mode='markers'
                            )
                        ],
                        'layout':go.Layout(
                            xaxis={'title':'Claim Amount'},
                            yaxis={'title':'Close Amout'},
                            hovermode='closest'
                            ),
                        'layout':{'title':'Scatter Chart'}
                        }
                        ,),
                    ])


table4 = dcc.Tab(label = 'Pie Chart', value='tab-empat',children =[
                    html.Div(children =[
                    dcc.Dropdown(id='pie',
                        options=[{'label' : i,'value' : i}for i in dftsa.select_dtypes('number').columns],
                        value='Claim Amount')
                    ],className='col-3'),
                    dcc.Graph(
                    id = 'contoh-graph-pie',
                    figure = {
                        'data':[
                            go.Pie(labels = ['Claim Type{}'.format(i) for i in list(dftsa['Claim Type'].unique())],
                                            values = [dftsa.groupby('Claim Type').mean()['Claim Amount'][i] for i in list(dftsa['Claim Type'].unique())],
                                            sort = False)
                            ],
                            'layout': {'title': 'Mean Pie Chart'}
                            }
                            )],)
