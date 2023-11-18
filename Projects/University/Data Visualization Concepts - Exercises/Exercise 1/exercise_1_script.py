#importing all the libraries
import pandas as pd
import numpy as np
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange
import bokeh.palettes as bp # uncomment it if you need special colors that are pre-defined
import datetime as dt
from math import pi

#output_file to create html file with the final visualization

output_file('dvc_ex1.html')

#Task 1: Data Pre-processing
#Read data into a dataframe using pandas

#if data file is in the same folder as the script or notebook, no path is needed
df = pd.read_csv("data.csv")

#Convert "pickup_datetime" attribute in the dataframe to datetime type for further processing
#Reference Links: 
    # https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])


#Split datetime object to months and hours, and do the following conversion for months:
    # 5 -> "May" 
    # 3 -> "March" , and so on.
#Reference links:
    # https://www.projectpro.io/recipes/split-datetime-data-create-multiple-feature-in-python
df['pickup_datetime_month'] = df['pickup_datetime'].dt.month
df['pickup_datetime_hour'] = df['pickup_datetime'].dt.hour

#conversion from number to name of the month

#Use months as stack names
stacks = ["jan","feb","march","april","may","june"]

df['pickup_datetime_month'] = df['pickup_datetime_month'].replace([1, 2, 3, 4, 5, 6], stacks)

#Calculate the total number of trips for each month grouped by hour(In other words calculate the stack values).
#Reference links:
    # https://www.geeksforgeeks.org/python-pandas-dataframe-groupby/#:~:text=groupby()%20function%20is%20used,of%20labels%20to%20group%20names.
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html 
    # https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.GroupBy.size.html

stack_val_jan = df[df['pickup_datetime_month']=='jan'].groupby(['pickup_datetime_hour']).size()
stack_val_feb = df[df['pickup_datetime_month']=='feb'].groupby(['pickup_datetime_hour']).size()
stack_val_march = df[df['pickup_datetime_month']=='march'].groupby(['pickup_datetime_hour']).size()
stack_val_april = df[df['pickup_datetime_month']=='april'].groupby(['pickup_datetime_hour']).size()
stack_val_may = df[df['pickup_datetime_month']=='may'].groupby(['pickup_datetime_hour']).size()
stack_val_june = df[df['pickup_datetime_month']=='june'].groupby(['pickup_datetime_hour']).size()

#Manipulate "pickup_datetime_hour" attribute for visualization purposes.
#Extract unique values for pickup_datetime_hour and create the time intervals(0 -> 0-1 , 23 -> 23-0 and so on) using string manipulation.

hours = list(range(0, 24))
hours_str = []

for x in hours:
    if x < 23:
        hours_str.append(str(x) + '-' + str(hours[x+1]))
    else:
        hours_str.append(str(x) + '-' + '0')


#Task 2: Data Visualization
#Using the information gathered from the data pre-processing step create the ColumnDataSource for visualization.


source = ColumnDataSource({'jan':stack_val_jan, 
                          'feb':stack_val_feb, 
                          'march':stack_val_march, 
                          'april':stack_val_april, 
                          'may':stack_val_may, 
                          'june':stack_val_june, 
                          'hours':hours, 'hours_str':hours_str})


# Visualize the data using bokeh plot functions

from bokeh.palettes import Category20

#creatig a tuple with 6 colors from Category20
colors = Category20[6]

p=figure(x_range=FactorRange(*hours_str), plot_height=800, plot_width=800, title='Number of trips in NYC')
p.yaxis.axis_label = "Number of trips"
p.xaxis.axis_label = "Hours"
p.sizing_mode = "stretch_both"
p.xgrid.grid_line_color = None

# Using vbar_stack to plot the stacked bar chart
p.vbar_stack(stacks, x='hours_str', source=source, color=colors, width=0.8)

# Add HoverTool. HoverTool should show the name of the month, the hours and the number of trips when the mouse hover on each bar.
#Reference Links:
    # https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool

hover = HoverTool(tooltips=[('Month', '$name'), ('Hours', '@hours_str'), ('Number of Trips', '@$name')])

p.add_tools(hover)


show(p)