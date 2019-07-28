
# coding: utf-8

# # Section 1
# The City of Baltimore maintains a database of parking citations issued within the city. More information about the dataset can be found here. You can download the dataset as a CSV file here. Unless stated otherwise, you should only consider citations written before January 1, 2019.

# ### Data cleaning and prep
# In[1]:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import fuzzywuzzy
from fuzzywuzzy import process

# #### initial read of file, drop unneccessary columns
# In[2]:
data = 'Parking_Citations.csv'
cols_keep = ['Citation', 'Make', 'ViolFine', 'ViolDate','OpenPenalty', 'PoliceDistrict']
cols_types = ['int64', 'str', 'float64', 'str', 'float64', 'str']
df = pd.read_csv(data, usecols=cols_keep, dtype=dict(zip(cols_keep, cols_types)))
# df = pd.read_csv(data, usecols=cols_keep, dtype=dict(zip(cols_keep, cols_types)), parse_dates=['ViolDate'])
df.head()

# #### Look at missing data
# In[3]:

# look at missing data
df.isnull().sum()

# Rather than dropping all missing fields, missing data in Make, ViolDate, and PoliceDistrict should be handled separately in each question related to these fields. Refer to each question's section for details.

# #### Convert data types
# In[4]:
# converting ViolDate column into python date time
df.ViolDate = pd.to_datetime(df.ViolDate, format='%m/%d/%Y %I:%M:%S %p', infer_datetime_format=True)
df.dtypes

# ### Q1.
# In[5]:
# There is no empty or null entries for violation fine, so we calculate the mean directly:
mean_vio_fine = df.ViolFine.mean()
print(round(mean_vio_fine,10))

# ### Q2. 
# #### Clean district entries
# In[6]:
# find unique values in district column:
districts = df.PoliceDistrict.unique()
print(districts)

# In[7]:
# replace 'Notheastern' with 'Northeastern'
df.PoliceDistrict = df.PoliceDistrict.replace('Notheastern', 'NORTHEASTERN')

# #### Calculate mean violation of each district group
# In[8]:
# group df by lowercased district name and find mean violation find
pd.set_option('display.precision',10)
dist_gp = df.groupby(df['PoliceDistrict'].str.upper()) # missing data is automatically dropped in 'groupby' method
dist_gp.mean().sort_values(by=['ViolFine'])


# ### Q3.
# #### Mask dataset, eliminate missing and uneccessary data
# In[9]:
# mask df by year to be between 2004 and 2014
ti_df = df.dropna(axis=0, subset=['ViolDate'])
yr_mask = (ti_df.ViolDate >= '2004-01-01') & (ti_df.ViolDate <'2015-01-01') # missing data will also be elminated by mask 
cite_yr = ti_df.loc[yr_mask]
cite_yr.sort_values(by=['ViolDate']).tail()


# In[10]:
# group masked df by year, calculate totals
# cite_yr.groupby(cite_yr.ViolDate.dt.year).count()
cite_count_yr = cite_yr['Citation'].groupby(cite_yr.ViolDate.dt.year).count()
cite_count_yr = cite_count_yr.reset_index(['ViolDate'])
cite_count_yr


# #### Run linear regression
# In[11]:
# use linear regression to plot citation over year
# X = cite_count_yr[['ViolDate']].as_matrix()
# X = cite_count_yr.drop('Citation', axis=1).values
# Y = cite_count_yr['Citation'].values

X = cite_count_yr.iloc[:, 0].values.reshape(-1, 1)
Y = cite_count_yr.iloc[:, 1].values.reshape(-1, 1)
lg = LinearRegression()
lg.fit(X,Y)
y_pred = lg.predict(X)

# visualize
plt.scatter(X,Y, color='red')
plt.plot(X, y_pred, color='blue')
plt.show()

# slope
coeff = lg.coef_
print("The slope of the prediction line is: {}.".format(round(float(coeff),10)))


# ### Q4. 
# # In[12]:
# There's 0 missing data in tihs field. filter citations with open penalty value > 0:
open_pen = df[(df.OpenPenalty > 0)]

# find 81th percentile
print('The 81st percentile of the dollar amount value of all open penalty fees is: {}.'.format(open_pen.OpenPenalty.quantile(0.81)))


# ### Q5. 
# #### Handle null values and mask dataset
# In[13]:
# drop null values
mk_df = df[['Citation', 'Make']]
mk_df = mk_df.dropna(axis=0, subset=['Make'])

# mask dataset
time_mask = (df.ViolDate >= '2017-01-01') & (df.ViolDate <'2018-01-01') # missing data will also be elminated by mask 
mk_df = mk_df.loc[time_mask]


# #### Clean up make entries
# In[14]:
# make all uppercase, remove tralining space
mk_df.Make = mk_df['Make'].str.upper()
mk_df.Make = mk_df['Make'].str.strip()

# see how many unique entries there are for make, explore values
mk_list1 = mk_df.Make.unique().tolist()
print(len(mk_list1))


# In[15]:
# drop anything that has 2 or more numbers in it (those are usually wrongly entered times and dates)
mk_df = mk_df[mk_df.Make.str.count(r'\d')<2]
mk_list = mk_df.Make.unique()
print(len(mk_list))
print(sorted(mk_list))


# In[16]:
# test fuzzywuzzy to pick a good score
test_makes = ['TOYOT', 'HONDA', 'FORD', 'NISSAN','ACURA']
for m in test_makes:
    test = fuzzywuzzy.process.extract(m, mk_list, limit=10, scorer=fuzzywuzzy.fuzz.WRatio)
    print(test)


# In[18]:
# generate a dictionary to map fuzzy make to accurate make
accurate_list = ['TOYOT', 'FORD','AUDI','MAZDA', 'HYUN'] # to start with
mk_dict = {}

for name in mk_list:
    # fuzz_socre = fuzzywuzzy.fuzz.token_sort_ratio(main_name['Name'].iloc[i],main_name['Name'].iloc[j])
    list_matches = fuzzywuzzy.process.extract(name, accurate_list, limit=10, scorer=fuzzywuzzy.fuzz.partial_token_sort_ratio)
    list_matches.sort(key=lambda x: x[1], reverse=True)
    if list_matches[0][1] <75:
        accurate_list.append(name)
        mk_dict[name] = name
    else:
        mk_dict[name] = list_matches[0][0]
        
print('total number of accurate make names: {}'.format(len(accurate_list)))
print('total number of make names: {}'.format(len(mk_dict)))


# In[19]:
# replace make names in the dataframe
mk_gp=mk_df
mk_gp['Make'].replace(mk_dict, inplace=True)
display(mk_gp.head())
print("cleaned number of makes:{}".format(len(mk_gp.Make.unique())))


# #### Group by new make to find top ones
# In[20]:
# Find the ten vehicle makes that received the most citations during 2017. 
top_ten = mk_gp.groupby(mk_gp.Make).count().sort_values(by=['Citation'],ascending=False).reset_index().head(10)
top_ten


# In the top 10 makes that reveive most citaitons, Japanese-made ones are: Honda, Toyota, Nissan, Acura.
# In[21]:
# What proportion of all citations were written for those vehicles?
jpn_cite = 70590+68729+50111+19505
tot_cite = mk_df.Citation.count()
print("The proportion of all citations that come from Japanese makes in top 10 makes list is:{}".format(jpn_cite/tot_cite))


# ### Q6. 
# #### Load and clean crime data
# In[22]:
# load data
crime = 'BPD_Part_1_Victim_Based_Crime_Data.csv'
cols = ['CrimeDate', 'Description', 'District', 'Total Incidents']
types = ['str', 'str', 'str', 'int64']
cf = pd.read_csv(crime, usecols=cols, dtype=dict(zip(cols, types)))
cf.head()


# In[23]:
# convert date to datetime64
cf.CrimeDate = pd.to_datetime(cf.CrimeDate, format='%m/%d/%Y', infer_datetime_format=True)
cf.dtypes

# In[24]:
# missing data
cf.isnull().sum()


# #### Determine how many instances of auto theft ocurred in each police district during 2015
# In[25]:
# time mask the dataframe
cf_15 = cf.loc[(cf.CrimeDate >= '2015-01-01') & (cf.CrimeDate <'2016-01-01')]

# look at unique values of Description and District column, see if entries are consistant
print(cf_15.Description.unique())
print(cf_15.District.unique())

# In[34]:
# filter out Auto Theft, clean names, group by district
auto_thft = cf_15.loc[cf_15['Description'].str.upper() == "AUTO THEFT"]
# dist_dict = {'NORTHEAST':'NORTHEASTERN','SOUTHEAST':'SOUTHEASTERN','NORTHWEST':'NORTHWESTERN', 'SOUTHWEST':'SOUTHWESTERN'}
# auto_thft.Description = auto_thft.Description.replace(dist_dict)
# auto_thft
theft_series = auto_thft['Total Incidents'].groupby(auto_thft.District).sum()
theft_series


# #### Determine the number of parking citations that were issued in each police district during the same year
# In[36]:
# apply time mask and clean up police district entries in citation table 
df_15 = df.loc[(df.ViolDate >= '2015-01-01') & (df.ViolDate <'2016-01-01')]
# df_15['PoliceDistrict'] = df_15['PoliceDistrict'].replace(np.nan, 'UNKNOWN')
df_15['PoliceDistrict'].fillna('UNKNOWN', inplace=True)
df_15.PoliceDistrict = df_15.PoliceDistrict.str.upper()
cite_series = df_15.Citation.groupby(df_15.PoliceDistrict).count()
cite_series

# #### Determine the ratio of auto thefts to parking citations for each district. Out of the nine police districts, what was the highest ratio?

# In[28]:
# merge auto theft table and citation table
combined = pd.concat([theft_series.reset_index(), cite_series.reset_index()], axis=1, sort=False)
combined

# In[29]:
# add a column for the ratio
combined['Ratio'] = combined['Total Incidents']/combined['Citation']
combined.sort_values(by=['Ratio'], ascending=False)
# The highest ratio is 0.3275563258 in Northwest District.
