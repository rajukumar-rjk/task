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

# data.head()

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

# line chart
plt.style.use('seaborn-darkgrid')
plt.plot(total_user_by_month_per, color='g')
plt.xlabel('MONTH')
plt.ylabel('% OF NEW USER')
plt.title('User acquisition rate by Month')

#bar chart
# a = total_user_by_month_per.plot(kind='barh')
# total_user_by_month_per['mnth_yr'].head() ['mnth_yr']
# a.set_xlabel("mnth_yr")
# a.set_ylabel("total unique user")
# a.set_title('% of new user by month')







################################################ 2.What is the month on month repeat rate?

#counting total no of booking by user and month
count_user_booking = data.groupby(['mnth_yr','profile_id']).size()

#create new data frame to work for q2
new_data = count_user_booking.to_frame(name = 'no_of_repeat').reset_index()



# no_of_repeat = new_data.groupby(['mnth_yr', 'repeatebyuser']).size()


#calculating % of user who made repeate
no_of_repeat_per = new_data.groupby(['mnth_yr', 'no_of_repeat']).size().groupby(level=0).apply(lambda x:
                                                 100 * x / float(x.sum()))

#Excluding percentage of usher who made just one order
df1 = no_of_repeat_per.to_frame(name='per').reset_index()
df1 = df1[df1.no_of_repeat != 1]

#pivot data to plot the line chart
ad = df1.pivot(index='mnth_yr',columns= 'no_of_repeat', values='per')




#ploting the chart stacked bar
# no_of_repeat_per['no_of_repeat']

# a = no_of_repeat_per.unstack().plot(kind='barh', stacked=True)
# a.set_ylabel("year-month")
# a.set_xlabel("% of user")
# a.set_title('Monthly repeat rate')



# line chart
plt.style.use('seaborn-darkgrid')
plt.plot(ad)
plt.xlabel('Year-Month')
plt.ylabel('% no of repeat')
plt.title('Monthly repeat rate')
plt.legend('2345', ncol=2, loc='upper left')



##################################### 6.Plot repeat frequency distribution by users

#no of booking by user
total_booking_by_user = data.groupby(["profile_id"]).count().sort_values("profile_id", ascending=False)



##plotting the chart
plt = total_booking_by_user.groupby('date_of_booking').size().plot(kind='bar')
plt.set_xlabel("No of booking")
plt.set_ylabel("No of user")
plt.set_title('repeat frequency distribution by users')
