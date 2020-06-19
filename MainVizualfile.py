# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import numpy as np
from navigation import bar_menu, navbar_menu


import pandas as pd
import plotly.graph_objs as go


app = dash.Dash()

external_stylesheets =['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
# import dataframe
df = pd.read_csv('Earthquakedatabase.csv')
features = df.columns[2:20]
opts = [{'label' :i, 'value':i} for i in features]

df['Date'] = pd.to_datetime(df['Date'])
#to arrange the date
dates = ['01-02-1964', '01-02-1968', '01-02-1972', '01-02-1976',
         '01-02-1980', '01-02-1995', '01-02-2000', '01-02-2005',
         '01-02-2010']
date_mark = {i : dates[i] for i in range(0,9)}

#bootstrap navbar
navbar = navbar_menu()
#DropDown

drop_down = html.P([
	html.Label("Choose a feature"),
	dcc.Dropdown(id = 'opt', options = opts, value = opts[0]['value'])
	],
	style = {'width': '400px', 'fontSize':'20px', 'padding-left' : '100px', 'display':'inline-block'})



# adding a header and a paragraph
header = html.Div([
		html.H1("EarthQuake data "),
		html.P("The Data is taken as based on simultaneously states as per Kagale !!")
		], style = {'padding':'30px', 'backgroundColor' : '#3aaab2'})



#rangeSlider
rangeslider = html.P([
	html.Label("Time Period"),
	dcc.RangeSlider(id = 'slider',
			marks = date_mark,
			min = 0,
			max = 8,
			value = [0,5])

	], style = {'width':'80%',
			'fontSize': '20%',
			'padding-left':'100px',
			'display': 'inline-block'})



# Launch the application
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Adding callback function to update the graph according to the choice of dropdown
@app.callback (Output('plot','figure'),
		 [Input('opt', 'value'),
		 Input('slider','value')])
def update_figure(input1, input2):
	df2 = df[(df.Date > dates[input2[0]]) & (df.Date < dates [input2[1]])]
	trace_1 = go.Scatter(x = df2.Date, y = df2['Magnitude'],
				name = 'Magnitude',
				line = dict(width = 2, color = 'rgb(229,151,50)')
				#mode = 'markers'
					)

	trace_2 = go.Scatter(x = df2.Date, y = df2[input1],
                        name = input1,
			line = dict(width = 2,color = 'rgb(106, 181, 135)')
                        #mode = 'markers'
					)

	fig = go.Figure(data = [trace_1, trace_2], layout = layout)

	return fig

#bar Chart

bar = bar_menu()
trace_scatter_plot = go.Bar(x=df['Date'], y=df['Depth'], name="the Depth")




#scatter plot
scatter = html.Div([
		dcc.Graph(id='plot1',
			figure={'data':[go.Scatter(
					x=df['Latitude'],
					y=df['Longitude'],
					mode='markers'
					)],
				'layout':go.Layout(title='Longitude and Latitude analysisy',
                xaxis={'type': 'log', 'title': 'Latitude'},
                yaxis={'title': 'Longitude'},
						hovermode='closest')
				}
				)
			]
#		style={'width':'30%','display':'inline-block'}
		)

# Desiging Card Function
def create_card(title, content):
	card = dbc.Card(
		dbc.CardBody(
			[
			html.H4(title, className="card-title",style={'font':20}),
			html.Br(),
			html.Br(),
			html.H2(content, className="card-subtitle",style={'font':20}),
			html.Br(),
			html.Br(),
			]
			),
			color="info", inverse=True
		)
	return(card)



# create Card Object

card4 = create_card("Number of Comment on Articles", "None Comments")
card3 = create_card("Number of Articles","None Articles")
card2 = create_card("Date", "Depth")
card1 = create_card("Depth Calculation", "Select Data to View")

@app.callback(Output('card1','children'),
		[Input('plot1','selectedData')])
def find_density(selectedData):
	#calculate the density as per selection of data
	pts = len(selectedData['points'])
	rng_or_1p = list(selectedData.keys())
	rng_or_1p.remove('points')
	max_x = max(selectedData[rng_or_1p[0]]['x'])
	min_x = min(selectedData[rng_or_1p[0]]['y'])
	max_y = max(selectedData[rng_or_1p[0]]['y'])
	min_y = min(selectedData[rng_or_1p[0]]['y'])
	area = (max_x-min_x)*(max_y-min_y)
	d = pts/area
	print ('value maxX:{}, value maxY:{}'.format (max_x, max_y))
	return create_card('Density = {:.2f}'.format(d), "Depth Per Area")


#density3 = html.Div([
#		html.H1(id='density',style={'paddingTop':2})
#		],style={'display':'inline-block','verticalAlign':'top'})


# create Card for Bootstrap layout with row and column
graphRow0 = dbc.Row([dbc.Col(id='card1', children=[card1], md=3), dbc.Col(id='card2', children=[card2], md=3), dbc.Col(id='card3',
		children=['card3'], md=3)])


# create a plotly Figure

trace_1 = go.Scatter(x = df.Date, y = df['Depth'],
                        name = 'Depth',
                        #line = dict(width = 2,color = 'rgb(229,151,50)')
				)
trace_2 = go.Scatter(x = df.Date, y = df['Magnitude'],
                        name = 'Depth',
                        #line = dict(width = 2,color = 'rgb(229,151,50)')
				)

def create_layout(words):
	layout = go.Layout(title = words, hovermode = 'closest')
	return layout
#fig_card_2 = go.Figure(data = [trace_1], layout = create_layout("Depth Per Day"))

layout = go.Layout(title = 'Time Series Plot', hovermode = 'closest')

# Function to create plot figure as per data and title
def create_figure(trace,phrase):
	layoutValue = go.Layout(title = phrase,  hovermode = 'closest' )
	figure = go.Figure(data = [trace], layout = layoutValue)
	return figure

# for calculating Depth Per day
fig_card_2 = create_figure(trace_1,"Depth Per Day")

# Magnitude per day
fig = create_figure(trace_2,"Magnitude")

# Bootstrap main Row
mainRow = dbc.Col(
	children=[dbc.Row(
		id='main',
		children=[
			dbc.Col(id='mainCol', children=[
				dbc.Row(children=[
					dbc.Col(id='card2', children=[dcc.Graph(id = 'card_depth', figure = fig_card_2,style={'height':'300px'})], md=10),
					dbc.Col(id='card1', children=[card1], md=2)
					#dbc.Col(id='card3', children=[card3], md=4)
				]),
				dbc.Row(children=[
					dbc.Col(id='char1', children=[dcc.Graph(id = 'plot', figure = fig)], md=12)
				]),
				dbc.Row(
					children=[
						dbc.Col(children=[drop_down], md=12)
					]
				),
				dbc.Row(
					children=[
						dbc.Col(children=[rangeslider], md=12)
					]
				)
			], md=9),
			dbc.Col(id='sideCol', children=[
				dbc.Row(children=[
					dbc.Col(id='card4', children=[scatter], md=12,),
				]),
				html.Br(),
				dbc.Row(children=[
					dbc.Col(id='chart2', children=[bar], md=12)
				])
			], md=3)
		]
	)],
	md=12
)

# creating a Dash layout
app.layout = html.Div([
#navigation button bar
html.Div([navbar], style={'backgroundColor':'black'}),


#the header Plot
header,

#the card
html.Br(),
mainRow,
])
# fro input togling data
def toggle_modal(input1, input2, is_open):
    if input1 or input2 :
        return not is_open
    return is_open

app.callback(
     Output("modalBlog", "is_open"),
    [Input("openBlog", "n_clicks"),Input("closeBlog", "n_clicks")],
    [State("modalBlog", "is_open")],
)(toggle_modal)



# Adding the server Clause

if __name__ == '__main__':
    app.run_server()
