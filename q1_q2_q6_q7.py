import pandas as pd

import dateutil
import datetime
import numpy as np

import matplotlib.pyplot as plt


# Load data
data = pd.read_csv('task.csv')

# rows the dataset
data['profile_id'].count()
data.dtypes



#convert data string to
data['date_of_booking'] = pd.to_datetime(data['date_of_booking'])



#creating booking month year field
data['mnth_yr'] = data['date_of_booking'].apply(lambda x: x.strftime('%Y-%m'))


#sorting data frame with month year
data = data.sort_values(by="mnth_yr")
data['mnth_yr'].value_counts().sort_index()




##################### 1.Please plot month on month User acquisition rate

#cereating a column having 0 (if user has alredy made booking in past) or 1 (if user is making first booking)
data['unique_user'] = np.where(data.duplicated('profile_id'), 0, 1)

data.head()

# data.to_csv("unique_user.csv",sep='\t', encoding='utf-8')
#creating new df to plot q1 chart (we just need two columns month-year and unique_user
df1 = data[['mnth_yr','unique_user']]

#calculating total user by month
total_user_by_month = df1.groupby(['mnth_yr']).sum()

#calculating total user (overall) to get month wise new user percentage.
total_user = df1['unique_user'].sum()



#calculating month wise percentage of new user
total_user_by_month_per = total_user_by_month.groupby(level=0).apply(lambda x:
                                                 100 * x / float(df1['unique_user'].sum()))

# line chart style
plt.style.use('seaborn-darkgrid')
plt.plot(total_user_by_month_per, color='g')
plt.xlabel('MONTH')
plt.ylabel('% OF NEW USER')
plt.title('User acquisition rate')

#bar chart
# a = total_user_by_month_per.plot(kind='barh')
# total_user_by_month_per['mnth_yr'].head() ['mnth_yr']
# a.set_xlabel("mnth_yr")
# a.set_ylabel("total unique user")
# a.set_title('% of new user by month')


# 2.What is the month on month repeat rate?

#counting total no of booking by user and month
count_user_booking = data.groupby(['mnth_yr','profile_id']).size()

#create new data frame to work for q2
new_data = count_user_booking.to_frame(name = 'no_of_repeat').reset_index()

# no_of_repeat = new_data.groupby(['mnth_yr', 'repeatebyuser']).size()


#calculating % of user who made repeate
no_of_repeat_per = new_data.groupby(['mnth_yr', 'no_of_repeat']).size().groupby(level=0).apply(lambda x:
                                                 100 * x / float(x.sum()))


#ploting the chart
a = no_of_repeat_per.unstack().plot(kind='bar', stacked=True)
a.set_ylabel("year-month")
a.set_xlabel("% of user")
a.set_title('month repeat rate')









# 6.Plot repeat frequency distribution by users

#no of booking by user
a = data.groupby(["profile_id"]).count().sort_values("profile_id", ascending=False)



##plotting the chart
plt = a.groupby('date_of_booking').size().plot(kind='bar')
plt.set_xlabel("No of booking")
plt.set_ylabel("No of user")
plt.set_title('repeat frequency distribution by users')



# 7.Using the data available, find out reasons why certain users are repeating and certain users are not?

"""
28% (Out of 16711) user have made booking more than once, but most of those user have made their first booking
in first 3 months which is Dec-17 to Feb-18(assuming they signed up betweeen these time period). Those
user also have bit better retention rate compare to user who made their first booking after Feb-18.

We have to find out what did happen between Dec-17 to Feb-18,  
1. Was there a specific marketing campaign that brought them in?
2. Did repeating user taking advantage of a promotion at sign-up?

"""