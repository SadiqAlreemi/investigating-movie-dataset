#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Investigate a Dataset (Replace this with something more specific!)
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# In this project, you choose the TMDB data set to investigations them, and this project is part of the requirements of getting a certificate (Data Analysis Nanodegree) from the Udacity platform.
# I will try to answer the following questions:
# 
# <ol>
# <li>Which genres are most popular from year to year?</li>
# <li>What kinds of properties are associated with films that have high revenues?</li>
# </ol>
# 

# In[5]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html

#importing important Libraries 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# ### General Properties

# In[6]:


# Load data from TMDb_movie_data.csv
df = pd.read_csv('TMDb_movie_data.csv')


# In[7]:


# Read the first five rows from TMDb_movie_data.csv
df.head()


# #### We do some statistic to understand data more 

# In[8]:


df.describe()


# #### We show data frame information like(columns, rows, data types)

# In[9]:


df.info()
print(' ')
print('Dataframe contains {} rows and {} columns'.format(df.shape[0],df.shape[1]))


# #### Find out the unique values in each column.

# In[10]:


df.nunique()


# In[11]:


df.hist(figsize=(13,13));


# #### Observation:
# After viewing the spreadsheet and focusing on the questions asked, the unnecessary data will be deleted and we will retain important data that will help us answer the questions. 
# 
# ----

# ### Data Cleaning (Removing the unused information from the dataset )
# 
# **We will take the following steps to clean up the data that is not important:**
# <ol>
#     <li>Remove unused columns.</li>
#     <li>Delete duplicate data in the table rows.</li>
#     <li>Replace the zero values to NAN in the Revenue and budget column as well as the runtime.</li>
#     <li>Change the data format in the Revenue and budget column.</li>
#     <li>Change the data format of the date column.</li>
# </ol>

# **1. Remove unused columns.**

# In[12]:


#creating a list of columb to be deleted
del_col=[ 'id', 'imdb_id', 'popularity', 'budget_adj', 'revenue_adj', 'homepage', 'keywords', 'overview', 'production_companies', 'vote_count', 'vote_average']

#deleting the columns
df= df.drop(del_col,1)

#previewing the new dataset
df.head(4)


# **2. Delete duplicate data in the table rows.**

# In[13]:


# First, we review the number of rows and columns 
rows, col = df.shape
print('There are {} rows and {} of columns in table.'.format(rows-1, col))


# In[14]:


# Second, we delete the repeating rows
df.drop_duplicates(keep ='first', inplace=True)
rows, col = df.shape


# In[15]:


# Finally, we review again the number of rows and columns 
rows, col = df.shape
print('There are {} rows and {} of columns in table.'.format(rows-1, col))


# We remove 1 row only.

# **3. Replace the zero values to NAN in the Revenue and budget column as well as the runtime.**

# In[16]:


# creating a seperate list of revenue and budget column
temp_list=['budget', 'revenue', 'runtime']

#this will replace all the value from '0' to NAN in the list
df[temp_list] = df[temp_list].replace(0, np.NAN)

#Removing all the row which has NaN value in temp_list 
df.dropna(subset = temp_list, inplace = True)

rows, col = df.shape
print('So after removing such entries, we now have only {} movies.'.format(rows-1))


# **4. Change the data format in the Revenue and budget column.**

# In[21]:


# First, checking the data types.
df.dtypes


# In[17]:


# Second, change Revenue and budget column data types from float64 to int64
change_type=['budget', 'revenue']
df[change_type]=df[change_type].applymap(np.int64)


# In[23]:


# Finally, checking the data types again.
df.dtypes


# **5. Change the data format of the release_data column.**#

# In[18]:


# Change the date on release_date column 
df.release_date = pd.to_datetime(df['release_date'])
df.head()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# ### Research Question 1 (What films have made the most profit?)

# In[19]:


# Use this, and more code cells, to explore your data. Don't forget to add
#   Markdown cells to document your observations and findings.

#insert function with three parameters(index of the column in the dataset, name of the column, value to be inserted)
df.insert(2,'profit_earned',df['revenue']-df['budget'])

#previewing the changes in the dataset
df.head(2)


# In[20]:


import pprint
#defining the function
def calculate(column):
    #for highest earned profit
    high= df[column].idxmax()
    high_details=pd.DataFrame(df.loc[high])
    
    #for lowest earned profit
    low= df[column].idxmin()
    low_details=pd.DataFrame(df.loc[low])
    
    #collectin data in one place
    info=pd.concat([high_details, low_details], axis=1)
    
    return info

#calling the function
calculate('profit_earned')


# > Column with id 1386 shows the highest earned profit i.e 2544505847	.
# >
# > Whereas the column with id 2244 shows the lowest earned profit i.e -413912431

# ### Research Question 2 : What is the average movie runtime?

# In[21]:


# defining a function to find average of a column
def avg_fun(column):
    return df[column].mean()
avg_fun('runtime')


# **Lets analyze the average** 

# In[22]:


#plotting a histogram of runtime of movies

#giving the figure size(width, height)
plt.figure(figsize=(9,5), dpi = 100)

#On x-axis 
plt.xlabel('Runtime of the Movies', fontsize = 15)
#On y-axis 
plt.ylabel('Nos.of Movies in the Dataset', fontsize=15)
#Name of the graph
plt.title('Runtime of all the movies', fontsize=15)

#giving a histogram plot
plt.hist(df['runtime'], rwidth = 0.9, bins =35)
#displays the plot
plt.show()


# <a id='conclusions'></a>
# ## Conclusions
# 
# > **Through our analysis of the data, it is clear to us the following:**
# <ul>
# <li>The highest profit (Avatar) film of the director (James Cameron), which amounted to income (2,781,505,847), which achieved net profit (2,544,505,847).</li>
# <li>The lowest profit (the Warrior's Way) of the director (Sngmoo Lee), which amounted to income (11,087,569), which achieved net loss (413,912,431).</li>
# <li>We also conclude that the film budget is not considered one of the most important factors of success, but there are other factors such as (Director-artists-Film type-duration of the film).</li>
# <li>We also infer from the analysis that the average operating time for most films is 109 minutes.</li>
# </ul>

# In[ ]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

