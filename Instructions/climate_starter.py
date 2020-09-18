
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt


# # Reflect Tables into SQLAlchemy ORM



# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[6]:


# Create the inspector and connect it to the engine
inspector = inspect(engine)


# In[7]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[8]:


# We can view all of the classes that automap found
#Base.classes.keys()
inspector.get_table_names()


# In[9]:


measurement_column= inspector.get_columns("measurement")
for i in measurement_column:
    print(i["name"],i["type"])


# In[10]:


station_column=inspector.get_columns("station")
for i in station_column:
  print(i["name"],i["type"])


# In[11]:


# Save references to each table
measurement=Base.classes.measurement
station=Base.classes.station


# In[12]:


# Create our session (link) from Python to the DB
session= Session(engine)


# # Exploratory Climate Analysis

# In[13]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results

# Calculate the date 1 year ago from the last data point in the database
precipitation_date=session.query(measurement.date).order_by(measurement.date.desc()).first()
print(precipitation_date)

prev_year = dt.date(2017,8,23) - dt.timedelta(days= 365)
print(prev_year)

# Perform a query to retrieve the date and precipitation scores
precipitation_dt= session.query(measurement.date, measurement.prcp).    filter(measurement.date >=prev_year).all()
precipitation_dt

# Save the query results as a Pandas DataFrame and set the index to the date column
precipitation_df=pd.DataFrame(precipitation_dt,columns=["date","precipitation"])
precipitation_df

# Sort the dataframe by date
precipitation_df= precipitation_df.sort_values(["date"],ascending= True)
precipitation_df.set_index(["date"],inplace=True)
precipitation_df


# Use Pandas Plotting with Matplotlib to plot the data
precipitation_df.plot(figsize=(7,7))
plt.tight_layout()
plt.xlabel("Date")
plt.ylabel("Rain")
plt.title("Precipitation Analysis")
plt.legend(["Precipitation"])
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#plt.savefig('Images/PrecipitationData.png')


# In[14]:


# Use Pandas to calcualte the summary statistics for the precipitation data
precipitation_df.describe()


# In[15]:


# Design a query to show how many stations are available in this dataset?

stations_total=session.query(measurement.station).distinct().count()
stations_total


# In[16]:


# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
active_stations=session.query(measurement.station,func.count(measurement.station)).                group_by(measurement.station).                order_by(func.count(measurement.station).desc()).all()
active_stations

# active_stations = session.query(measurement.station,
#                   func.count(measurement.station)).all()
# active_stations

# active_stations = session.query(measurement.station,
#                   func.count(measurement.station))\
# .group_by(measurement.station).all()
# active_stations


# In[17]:


# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of the most active station?


# highest_temp=session.query(func.max(measurement.tobs)).\
#             filter(measurement.station==active_stations[0][0]).order_by(func.max(measurement.tobs)).all()
# highest_temp

# lowest_temp=session.query(func.min(measurement.tobs)).\
#              filter(measurement.station==active_stations[0][0]).order_by(func.min(measurement.tobs)).all()
# lowest_temp

# average_temp=session.query(func.avg(measurement.tobs)).\
#              filter(measurement.station==active_stations[0][0]).order_by(func.avg(measurement.tobs)).all()
# average_temp

# print(f"The highest temperature of the most active station is {highest_temp},  the lowest temperature is {lowest_temp} 
#      average temperature {average_temp}')
# # i = 0
# # while i < len(active_stations):
# #     print(session.query(measurement.station, measurement.tobs).\
# #     filter(measurement.station == active_stations[i][0]).all())
# #     i += 1

# # temp_data= session.query(measurement.station, measurement.tobs).\
# #     filter(measurement_table.station == active_stations[0][0] ).all()

# # temps = session.query(measurement.tobs).group_by(measurement.station).limit(1).all()
# # temps
# # # lowest_temp=
# # # average_temp=
i = 0
while len(active_stations) > i:
    print(active_stations[i][0])
    print(session.query(func.max(measurement.tobs)).    filter(measurement.station == active_stations[i][0]).order_by(func.max(measurement.tobs)).all())
    print(session.query(func.min(measurement.tobs)).    filter(measurement.station == active_stations[i][0]).order_by(func.min(measurement.tobs)).all())
    print(session.query(func.avg(measurement.tobs)).    filter(measurement.station == active_stations[i][0]).order_by(func.avg(measurement.tobs)).all())
    if active_stations[i][0] == active_stations[0][0]:
        break


# In[18]:


# Choose the station with the highest number of temperature observations.

# Query the last 12 months of temperature observation data for this station and plot the results as a histogram


# In[19]:


temp_obs =[]
i = 0
while len(active_stations) > i:
    temp_obs.append(session.query(measurement.station, func.count(measurement.tobs)).    filter(measurement.station == active_stations[i][0]).                    order_by(func.count(measurement.tobs)).all())
    i+=1
print(temp_obs[0])



# In[20]:


last_twelve=session.query(measurement.tobs).            filter(measurement.date>=prev_year).filter(measurement.station=="USC00519281").all()
last_twelve
            
last_twelve
twelve_df=pd.DataFrame(last_twelve, columns= (["tobs"]))
twelve_df.head()


# In[21]:


bins = 12
twelve_df.plot.hist(last_twelve,bins)
plt.ylim(0,80)


# In[22]:


n_bins = 12
x = twelve_df['tobs']
fig, ax = plt.subplots()
ax.hist(x, bins=n_bins)


# ## Bonus Challenge Assignment

# In[24]:


# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

# function usage example
print(calc_temps('2012-02-28', '2012-03-05'))


# In[25]:


# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.
pyend_date=dt.date(2012,2,28)
pystart_date= pyend_date - dt.timedelta(days=365)
print(pystart_date,pyend_date)

def calc_temps(pystart_date, pyend_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).        filter(measurement.date >= pystart_date).filter(measurement.date <= pyend_date).all()

#function usage example
print(calc_temps('2012-02-28', '2012-02-28'))


# In[26]:


# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)

tmax = 73
tmin = 66
tavg = 70.375
difftemp = tmax - tmin
print(difftemp)

plt.figure(figsize=(4, 8))
plt.tick_params(bottom='off', top='off', labelbottom='off')
plt.bar(1, tavg, yerr=difftemp)
plt.ylabel('Temp (F)')
plt.title('Trip Avg Temp')
plt.show()


# In[51]:


# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation
pyend_date=dt.date(2012,2,28)
pystart_date= pyend_date - dt.timedelta(days=365)
#print(pystart_date,pyend_date)
total_rainfall=session.query(measurement.station,measurement.prcp,station.name,station.latitude, station.longitude, station.elevation).                filter(measurement.date>=pystart_date).                filter(measurement.date<=pyend_date).                group_by(measurement.station).                order_by(measurement.prcp.desc()).all()
print(f"Here are all of the Stations (in descending order) with the total number of rainfall between {pystart_date} & {pyend_date}:")
total_rainfall


# In[53]:


# Create a query that will calculate the daily normals 
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
    
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", measurement.date) == date).all()
    
daily_normals("01-01")


# In[85]:


# calculate the daily normals for your trip
# push each tuple of calculations into a list called `normals`

# Set the start and end date of the trip

# Use the start and end date to create a range of dates

# Stip off the year and save a list of %m-%d strings

# Loop through the list of %m-%d strings and calculate the normals for each date# listing the dates for vacation

Vacation_dates = ["02-28", "02-29", "03-01", "03-02", "03-03","03-04","03-05"]
normals = []
# returning avg, min, max rainfall for Hawaii vacation
for i in Vacation_dates:
    vacation = {}
    vacation["Date"] = "{}".format(i)
    daily_normal = daily_normals(i)
    vacation["Min"] = daily_normal[0][0]
    vacation["Avg"] = round(daily_normal[0][1],2)
    vacation["Max"] = daily_norm[0][2]
#print(vacation)
    normals.append(vacation)
#print(normals)

vacations_df = pd.DataFrame(normals)
vacations_df


# In[86]:


# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index
vacations_df.set_index("Date")


# In[88]:


# Plot the daily normals as an area plot with `stacked=False`
vacations_df.plot(kind="area",alpha = 0.5, stacked = False)


# In[ ]:




