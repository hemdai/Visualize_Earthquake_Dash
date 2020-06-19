# -*- coding: utf-8 -*-

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import numpy as np

# Data Source
df = pd.read_csv('NewEarthquakedatabase.csv')

#Create a navbar for the page
def navbar_menu():
	navbar = dbc.NavbarSimple(children=[
		dbc.Button("Home", id="home", size="lg"),
		dbc.Button("DataSet",id="DataSet", size="lg",href="https://www.kaggle.com/usgs/earthquake-database"),
		dbc.Modal(
		[
		  dbc.ModalHeader("BLOG"),
		  dbc.ModalBody("It's the body"),
		  dbc.ModalFooter(dbc.Button("Close",id="closeBlog",className="ml-auto"),),

		], id="modalBlog",
		),

	    ],
	    color="grey",
	    dark=True,
	)
	return navbar


# function for Bar Menu
# calculate the average of each value and ploting it with graph
def bar_menu():
	bar = dcc.Graph(id = "3",
        figure ={"data": [{
                          'x':['Depth ','Magnitude','Longitude','Latitude'],
                          'y':[np.average(df['Depth']),np.average(df['Magnitude']),np.average(df['Longitude']),np.average(df['Latitude'])],
                          'name':'SF Zoo',
                          'type':'bar',
                          'marker' :dict(color=['#D9CB04','#05C7F2','#D90416','#D9CB04']),
                  }],
                "layout": {
                      "title" : dict(text ="Average Calculations",
                                     font =dict(
                                     size=30,
                                     color = 'white')),
                      "xaxis" : dict(tickfont=dict(
                          color='white')),
                      "yaxis" : dict(tickfont=dict(
                          color='white')),
                      "paper_bgcolor":"#000000",
                      "plot_bgcolor":"#000000",
                      "width": "350",
		      "height": "350",
                      #"grid": {"rows": 0, "columns": 0},
                      "annotations": [
                          {
                              "font": {
                                  "size": 30
                              },
                              "showarrow": False,
                              "text": "",
                              "x": 0.4,
                              "y": 0.4
                          }
                      ],
                      "showlegend": False
	                  }
	              }
			)
	return bar


