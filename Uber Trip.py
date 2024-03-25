#import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

#load dataset
df = pd.DataFrame
df = pd.read_csv('/Users/valentinanguyen/Library/CloudStorage/GoogleDrive-syd682@mocs.utc.edu/My Drive/School/grad/Spring 24/CPSC 5175 (1)/EDA/Uber Request Data.csv')
df

#print basic info of DF
df.info()
df.head()



#clean request time and drop time columns


#seperate Request timestamp into two columns: req_date and req_time
#str.split split a string into a list of strings.t takes two argument: a separator and a maximum number of splits. The separator is the character or string that is used to split the string.

df[['req_date','req_time']] = df['Request timestamp'].str.split(' ', expand=True)
df


#seperate Drop timestamp into two columns: drop_date and drop_time
#str.split split a string into a list of strings.t takes two argument: a separator and a maximum number of splits. The separator is the character or string that is used to split the string.

df[['drop_date','drop_time']] = df['Drop timestamp'].str.split(' ', expand=True)
df


#change all the date and time columns from string types into date time format

#note: if you dont put the dayfirst parameter to be true, it will lead to this warning: <ipython-input-80-c07dfac511da>:19: UserWarning: Parsing dates in DD/MM/YYYY format when dayfirst=False (the default) was specified. This may lead to inconsistently parsed dates! Specify a format to ensure consistent parsing.
#The warning message is telling you that you are trying to parse dates in the DD/MM/YYYY format, but you have not specified the dayfirst argument. By default, dayfirst is False, which means that Python will interpret the first two digits of the date as the month. If you want Python to interpret the first two digits as the day, you need to set dayfirst to True.

#pd.to_datetime converst string date times into datetime objects

df['req_date'] = pd.to_datetime(df['req_date'],dayfirst=True)
df['req_time'] = pd.to_datetime(df['req_time'],dayfirst=True)
df['drop_date'] = pd.to_datetime(df['drop_date'],dayfirst=True)
df['drop_time'] = pd.to_datetime(df['drop_time'],dayfirst=True)

df.info()

#convert dates to MM/DD/YYYY

df['req_date'] = df['req_date'].dt.strftime('%m/%d/%Y')
df['drop_date'] = df['drop_date'].dt.strftime('%m/%d/%Y')

#convert times to HH:MM am/pm
#dt.strftimeconvert datetime objects in a panda series to a specified date format
df['req_time'] = df['req_time'].dt.strftime('%I:%M %p')
df['drop_time'] = df['drop_time'].dt.strftime('%I:%M %p')


#remove 'Request timestamp' and 'Drop timestamp' columns
#df.drop used to remove rows or columns not needed or to create a new DF with specific subsets of the data
df = df.drop(columns=['Request timestamp','Drop timestamp'])

df



#create pivot table to count num of occurences
#pivot tables are regular tables used in data analysis, reg tables are used for organization
dups = df.pivot_table(index=['req_date'],aggfunc='size')
print(dups)

#print avg
avg_num_req = dups.mean()
print(avg_num_req)

#change dates to the days of the week
#pd.to_datetime converst string date times into datetime objects
#.index.day_name changes dates to days of the week
dups.index = pd.to_datetime(dups.index)
day_names = dups.index.day_name()

#plot avg
plt.plot(day_names, dups, marker='o')
plt.axhline(y = avg_num_req, color='blue',linestyle= '--')
plt.title('Number of Uber Requests Per Day')
plt.xlabel('Days of the Week')
plt.ylabel('Number of Requests')
plt.annotate('Avg Number of Requests',('Thursday',1346), color = 'black', size='7.5')
plt.show()


#Calculate overall distribution of each trip status

df['req_date'] = pd.to_datetime(df['req_date'],format='%m/%d/%Y')
df['req_time'] = pd.to_datetime(df['req_time'],format='%I:%M %p')
df['drop_date'] = pd.to_datetime(df['drop_date'],format='%m/%d/%Y')
df['drop_time'] = pd.to_datetime(df['drop_time'],format='%I:%M %p')

  #add a new column to store the day of the week
  #dt.day_name used to get the day name from a datetime object. The function returns the name of the day of the week

df['Day']= df['req_date'].dt.day_name()

#convert dates to MM/DD/YYYY

df['req_date'] = df['req_date'].dt.strftime('%m/%d/%Y')
df['drop_date'] = df['drop_date'].dt.strftime('%m/%d/%Y')

#convert times to HH:MM am/pm

df['req_time'] = df['req_time'].dt.strftime('%I:%M %p')
df['drop_time'] = df['drop_time'].dt.strftime('%I:%M %p')

df

#count the number of occurances of each trip status by day
#value_counts() used to count the number of times each unique value appears in a Series or DataFrame. It returns a Series containing the counts of each unique value. The resulting object is in descending order, with the most frequently-occurring element first.

trip_stat_dist = df['Status'].value_counts()
print(trip_stat_dist)

#plot
#.index object refers to the object's index, or the values that are plotted on the x-axis. It can be accessed using the syntax ax.index, where ax is the Axes object.
#.values To get the values of a Matplotlibplot, you can use the .values attribute. This will return a NumPy array of the values of the plot.

plt.bar(trip_stat_dist.index,trip_stat_dist.values)
plt.title("Overall Trip Status Frequency")
plt.xlabel('Trip Status')
plt.ylabel('Frequency')
plt.show()


#further group the data by day of the week to analyze the distribution of trip statuses per day.
#df.groupby() used for data aggregation (.size,.sum,etc...)  used for grouping the data according to the categories and applying a function to the categories.
#size() a method that returns the number of elements in a DataFrame or Series. When used in combination with groupby(), it returns a Series containing the number of occurrences of each group.
#unstack() * seebelow *

trip_stat_by_day_dist = df.groupby(['Day','Status']).size().unstack()
print(trip_stat_by_day_dist)

print(trip_stat_by_day_dist.index)

#days of the week need to be in order
#.reindex(): used to change the index labels of a DataFrame. It can be helpful when you want to reorder the rows, add new rows with missing index labels, or remove existing rows.
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday']
trip_stat_by_day_dist = trip_stat_by_day_dist.reindex(day_order)
print(trip_stat_by_day_dist)

#reorder status order
stat_order = ['Trip Completed','No Cars Available', 'Cancelled']
trip_stat_by_day_dist = trip_stat_by_day_dist[stat_order]

#plot
#this is a multiindex DF...multiple levels or rows or columns...used to assign a list, series, or another data frame as the index of a given data frame. It is particularly useful when combining multiple data frames, allowing for easy modification of the index.

trip_stat_by_day_dist.plot(kind='barh')
plt.title("Distribution of Trip Status by Day")
plt.xlabel("Frequency")
plt.ylabel("Days of the Week")
plt.show()




#aggregate data by time intervals (hourly)

df.info()

df['req_time'] = pd.to_datetime(df['req_time'],format='%I:%M %p')

df['Hour'] = df['req_time'].dt.hour
print(df['Hour'])

#group data by hour and count request volume
req_vol_by_hr = df.groupby('Hour').size()
print(req_vol_by_hr)

#plot
req_vol_by_hr.plot(kind='line')
plt.title('Request Volume per Hour')
plt.xticks(np.arange(0,25, step = 5))
plt.xlabel('24 Hour Period')
plt.ylabel('Number of Requests')




df['req_date'] = pd.to_datetime(df['req_date'],format='%m/%d/%Y')
df['req_time'] = pd.to_datetime(df['req_time'],format='%I:%M %p')
df['drop_date'] = pd.to_datetime(df['drop_date'],format='%m/%d/%Y')
df['drop_time'] = pd.to_datetime(df['drop_time'],format='%I:%M %p')

#duration
duration = df['drop_time']-df['req_time']
print(duration)
#make a new column
df['duration']= duration

#import datetime
#
from datetime import datetime,timedelta
dur_mins = duration.dt.total_seconds()/60


#avg duration
avg_duration = np.mean(dur_mins)
print(avg_duration)


