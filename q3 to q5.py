import pandas as pd
import dateutil
import datetime
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('task.csv')


df['date_of_booking'] = pd.to_datetime(df['date_of_booking'])

# 3.Please define and measure the following repeat rates for each month
# 30-Day repeat rate
# 60-Day repeat rate
# 90-Day repeat rate



# creating booking period column based on booking date
#for 30 days repeat rate
df['booking_period'] = df.date_of_booking.apply(lambda x: x.strftime('%Y-%m'))


# for 60 days ()
# df['booking_period'] = df.date_of_booking.apply(lambda x: str(x.year)+'-'+str((x.month -1)// 2 * 2 + 1 ))

# 90-Day repeat rate
# df['booking_period'] = df.date_of_booking.apply(lambda x: str(x.year)+'q'+str((x.month-1)// 3 * 3 + 1 ))


# 120 Day repeat rate
df['booking_period'] = df['date_of_booking'].apply(lambda x: str(x.year)+'q'+str(x.quarter))


#creating a column cohort_group group based on their first booking
df.set_index('profile_id', inplace=True)
df['cohort_group'] = df.groupby(level=0)['date_of_booking'].min().apply(lambda x: x.strftime('%Y-%m'))
df.reset_index(inplace=True)



# aggregating data by cohort_group and booking_period
grouped = df.groupby(['cohort_group', 'booking_period'])

# counting the unique users, total booking per cohort group and booking period
cohorts = grouped.agg({'profile_id': pd.Series.nunique,
                       'transaction_id': pd.Series.nunique})


# make the column names more meaningful
cohorts.rename(columns={'profile_id': 'TotalUsers',
                        'transaction_id': 'TotalBooking'}, inplace=True)

# assing the CohortPeriod to each Cohort Group
def cohort_period(df):
    df['CohortPeriod'] = np.arange(len(df)) + 1
    return df

cohorts = cohorts.groupby(level=0).apply(cohort_period)

# reindex the DataFrame
cohorts.reset_index(inplace=True)
cohorts.set_index(['cohort_group', 'CohortPeriod'], inplace=True)

# create a Series holding the total size of each CohortGroup
cohort_group_size = cohorts['TotalUsers'].groupby(level=0).first()
cohort_group_size.head()


cohorts['TotalUsers'].unstack(0).head()

#calculating percentage
user_retention = cohorts['TotalUsers'].unstack(0).divide(cohort_group_size, axis=1)

user_retention.head(10)

#plotting the chart
sns.set(style='white')

plt.figure(figsize=(12, 8))
plt.title('Cohorts: User Retention')
plt.xlabel('User month no')
plt.ylabel('User first booking')
sns.heatmap(user_retention.T, mask=user_retention.T.isnull(), annot=True, fmt='.0%');

# 4.What is the best repeat rate metric among the above to follow and why?
"""

30-days repeat rate chart show 4-5% user retention in last 6 months. which I believe is very low at 
business point of view. Especially when our almost 35% user came in first 3 month (q1 chart shows) 
i.e It is not easy to get new user.

So even though 30-days matric not showing good but I still believe we should fallow 30-days metric. 


"""

# 5.Define churn period for this business and measure monthly churn rate
"""
Churn is one minus the retention rate as a percentage (month 1 retantion rate - month 2 retantion rate). 
I have already plotted 30-days retention chart for Q3 and that can help to see the churn.

Retention chart shows overall we have churn of 93 % from user's 1st month to their 2nd month and 
then it goes up/down by 1-2% till the end. 

I have notice that chrun goes donw or remain the same in user's 3rd month from their first booking then every 2nd month.


"""