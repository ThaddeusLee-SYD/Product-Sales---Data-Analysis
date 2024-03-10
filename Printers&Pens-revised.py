# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 10:49:01 2024

@author: lee
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import iqr


sales_df = pd.read_csv("product_sales.csv")


'''
Data Validation

'''
# take a look at first few rows
print(sales_df.head())

# prints data types of each column and missing values
print(sales_df.info())

# prints descriptive statistics for each numeric column
print(sales_df.describe())


# Shape of data frame - contains 15000 rows, 8 columns.
print(sales_df.shape)


'''
Note:- go through each column and detail steps taken to clean dataset
'''


# print number of NAN values in each column
print(sales_df.isna().sum()) # revenue column has 1074 missing values

# Week Column
print(sales_df['week'].value_counts())


# Sales Method Column
print(sales_df['sales_method'].unique())
# Sales methods in column Email, Email + Call, em + call, email
# Should only be 3 sales methods

# customer id
print(sales_df['customer_id'].nunique())

# nb_sold Column
print(sales_df['nb_sold'].value_counts())
print(sales_df['nb_sold'].value_counts().sum())



# revenue column
print(sales_df['revenue'].value_counts())
print(sales_df['revenue'].value_counts().sum())
print(sales_df['revenue'].unique())

# Years as Customer Column

print(sales_df['years_as_customer'].value_counts())
print(sales_df['years_as_customer'].unique())


sales_df = sales_df[(sales_df['years_as_customer']!=47) & (sales_df['years_as_customer']!=63)]




# nb_site_visits Column
print(sales_df['nb_site_visits'].value_counts())
print(sales_df['nb_site_visits'].unique())



# state Column
print(sales_df['state'].unique())
print(sales_df['state'].nunique()) # prints number of unique data points - 50
print(sales_df['state'].value_counts().sum())
# We can see that the state column contains no errors in spelling and that no correction is necessary

'''
tidying messy columns and missing values
'''
# Tidy sales_method column


sales_df['sales_method'] = sales_df['sales_method'].str.replace('em + call', 'Email + Call')
sales_df['sales_method'] = sales_df['sales_method'].str.replace('email', 'Email')


print(sales_df['sales_method'].unique())
print(sales_df['sales_method'].value_counts())
print(sales_df['sales_method'].value_counts().sum())



# Prints percentage of NAN values in revenue per sales_method
print(sales_df.groupby("sales_method")['revenue'].apply(lambda x: x.isnull().mean()))
# Call            0.036477
# Email           0.072864
# Email + Call    0.135692



# We can just delete the rows with missing values with the dropna method.
sales_df = sales_df.dropna()

# verify
print((sales_df.isna().sum()))
print(sales_df.shape)
print(sales_df.dtypes)


'''
Exploratory Data Analysis

We need to know:
- How many customers were there for each approach?
- What does the spread of the revenue look like overall? And for each method?
- Was there any difference in revenue over time for each of the methods?
- Based on the data, which method would you recommend we continue to use? Some
of these methods take more time from the team so they may not be the best for us
to use if the results are similar.

'''



# plot count of weeks since product was launched
a= sns.countplot(data=sales_df, x='week')
a.set_title('Fig1: Number of Sales in Weeks since product Launched')
plt.show()



# Histogram of nb_sold
b= sales_df['nb_sold'].plot.hist()
b.set_title('Fig2: Frequency of New Porducts Sold')
b.set_xlabel('New Porducts')
plt.show()



# plot count of years_as_customer
c = sales_df['years_as_customer'].value_counts().plot.bar(figsize=(10,5))
c.set_title('Fig3: Barplot -  Customers by Number of Years')
c.set_xlabel('Years as customers')
plt.show()

#NOTE: Most  customers are new customers


# Histogram of nb_site_visits
d= sales_df['nb_site_visits'].plot.hist(bins=20)
d.set_title('Fig4: Frequency of Website visits from Customer')
plt.show()


sales_df['nb_site_visits'].value_counts()


# state column
print(sales_df['state'].value_counts())



e = sns.countplot(data=sales_df ,x='state', hue='state', order=sales_df['state'].value_counts().iloc[0:10].index)
e.tick_params(axis='x', rotation=45)
e.set_title('Fig5: Top 10 States for Orders')
plt.show()



# We can see the number of orders per sales method from each state.
sales_method_location = sales_df.groupby('sales_method')['state'].value_counts()
print(sales_method_location)


'''
1. - How many customers were there for each approach?
'''
print(sales_df['sales_method'].value_counts())

#Email           6922
#Call            4781
#Email + Call    2223


f=sns.countplot(data=sales_df, x='sales_method', hue='sales_method')
f.set_title('Fig6: Count Plot - Broken Down Per Sales Method')
plt.show()


'''
2. - What does the spread of the revenue look like overall? And for each method?
'''

#### Overall spread of revenue

# Calculating min, max, mean and median of total revenue
sales_df['revenue'].agg(['min', 'max', 'mean', 'median'])
Overall_revenue_IQR = iqr(sales_df['revenue'])
print(Overall_revenue_IQR)
# Calculating inter-quartile range of 0, 0.25, 0.5, 0.75, and 1
sales_df['revenue'].quantile([0, 0.25, 0.5, 0.75, 1])

# histplot of overall revenue
g = sns.histplot(data=sales_df, x='revenue')
g.set_title('Fig7: Revenue Frequency Distribution')
plt.show()




# Boxplot of overall revenue
g = sns.boxplot(data=sales_df, x='revenue')
g.set_title('Fig7.2: Boxplot - Overall Revenue')
plt.show()




#### overall spread of each sales method

print(sales_df.groupby('sales_method')['revenue'].mean())
print(sales_df.groupby('sales_method')['revenue'].agg(['min', 'max', 'mean', 'median']))
print(sales_df.groupby('sales_method')['revenue'].quantile([0, 0.25, 0.5, 0.75, 1]))

call = sales_df.loc[sales_df['sales_method']=='Call', 'revenue']
email = sales_df.loc[sales_df['sales_method']=='Email', 'revenue']
email_call = sales_df.loc[sales_df['sales_method']=='Email + Call', 'revenue']

print('Call IQR: ', iqr(call))
print('Email IQR: ', iqr(email))
print('Email + Call IQR: ', iqr(email_call))




# Boxplot of revenue by sales method
h=sns.boxplot(data=sales_df, x='sales_method', y='revenue', hue='sales_method')
h.set_title('Fig8: Boxplot - Revenue by Sales Method')
plt.show()



#creates dataframe where revenue is totalled across sales methods
revenue_sum = sales_df.groupby('sales_method')['revenue'].sum().to_frame()


i = sns.barplot(data=revenue_sum, x=revenue_sum.index, y='revenue', order=['Email', 'Email + Call', 'Call'], hue='revenue')
i.set_title('Fig9: Total Revenue by Sales Method')
plt.legend([],[], frameon=False)
plt.show()



## did not use
#j=sns.barplot(data=sales_df, x='sales_method', y='revenue', hue='sales_method')
#j.set_title('Bar Plot - Revenue per Sales Method')
#plt.show()
#plt.savefig('Bar Plot - Revenue per Sales Method.png');



j=sns.histplot(data=sales_df, x='revenue', hue='sales_method', fill=True, 
               alpha=0.5, linewidth=0, kde=True)
j.set_title('Fig10: Density Plot of Revenue by Sales_method')
plt.show()




#The purpose of a density plot is to give you a visual representation of the underlying distribution of the data. It can help you understand the shape and spread of the data and identify any unusual values or outliers. It can also be used to compare the distribution of multiple variables or groups.





'''
3. - Was there any difference in revenue over time for each of the methods?
'''
#The below pivot table shows the means and medians of revenue of each sales method per week.
revenue_per_week = sales_df.groupby(['week', 'sales_method'])['revenue'].agg(['mean', 'median']).unstack()


# Average Revenue per sales method
sales_df.groupby('sales_method')['revenue'].mean().to_frame()


# Line Plot plot of revenue in each sales method by new products sold
k=sns.lineplot(data=sales_df, x="week", y="revenue", hue="sales_method")
k.set_title('Fig11: Line Plot - Revenue from Each Sales Method by Week')
plt.show()




#The below pivot table shows the means and medians of nb_sold of each sales method per week.
nb_sold_week = sales_df.groupby(['week', 'sales_method'])['nb_sold'].agg(['mean', 'median']).unstack()
# Line Plot plot of revenue in each sales method by new products sold
l=sns.lineplot(data=sales_df, x="week", y="nb_sold", hue="sales_method")
l.set_title('Fig12: Line Plot - Number of Products Sold from Each Sales Method by Week')
plt.show()




# Line Plot plot of revenue in each sales method by new products sold
m=sns.lineplot(data=sales_df, x="nb_sold", y="revenue", hue="sales_method")
m.set_title('Fig13: Line Plot - Revenue by Number of New Products Sold')
plt.show()





########################################################################

### Did Not Use
# multi-plot of revenue density in each sales method week by each week
#l = sns.FacetGrid(sales_df, col="week", hue='sales_method', height=2.5, col_wrap=3)
#l.map(sns.kdeplot, "revenue")
#l.fig.suptitle('Density of Revenue by Sales Method Per Week')
#plt.legend()
#plt.savefig('Density of Revenue by Sales Method Per Week.png');


### Did Not Use
# plot of revenue in each sales method in each week
#m=sns.barplot(    data=sales_df, x="sales_method", y="revenue", hue="week")
#m.set_title('Bar Plot: Total Revenue by Sales Method Per Week')
#plt.show()
#plt.savefig('Bar Plot: Total Revenue by Sales Method Per Week.png')



### Did not use
# multi-plot of revenue density per week
#p = sns.FacetGrid(sales_df, col="week", height=2.5, col_wrap=3)
#p.map(sns.kdeplot, "revenue")
#p.fig.suptitle('Density of Total Revenue by Week')
#plt.show()
#plt.savefig('Density of Total Revenue by Week.png');


### did not use
# multi-plot of revenue density in each sales method week by each week
#q = sns.FacetGrid(sales_df, col="week", hue='sales_method', height=2.5, col_wrap=3)
#q.map(sns.kdeplot, "revenue")
#q.fig.suptitle('Density of Revenue per Sales Method by Week')
#plt.legend()
#plt.show()
#plt.savefig('Density of Revenue per Sales Method by Week.png');

#########################################################################

'''
APPENDICES
'''

# Below we convert the 'sales_method' column into an integer column called 'sales_method_int'
# For our new column, 'sales_method_int', each sales method is assigned the corresponding number:
# Email = 0
# Call = 1
# Email + Call = 2

sales_df['sales_method_int'] = sales_df['sales_method'].replace(['Email', 'Call', 'Email + Call'], [0, 1, 2])
sales_df.head()

# We then select columns where data types are float or integer and create a new dataframe called sales_numbers
sales_numbers = sales_df.select_dtypes(['int', 'float'])
sales_numbers.head()


# We then create a heatmap that displays the correlation between each of the columns.
n=sns.heatmap(data=sales_numbers.corr(), annot=True)
n.set_title('Correlation Coefficient Between Columns')
plt.show()






# plot a scatter plot with regression line for website visits and products sold
e = sns.lmplot(data=sales_df, x='nb_site_visits', y='nb_sold')
e.fig.suptitle('Fig14: Correlation of Website Visits to New Products Sold')
plt.show()
plt.savefig('Fig14-CorrelationofWebsiteVisitstoNewProductsSold.png');


#Correlation Co-efficient of nb_site_visits and nb_sold
print(sales_df['nb_site_visits'].corr(sales_df['nb_sold']))

sales_method_location = sales_df.groupby('sales_method')['state'].value_counts()
print(sales_method_location)
