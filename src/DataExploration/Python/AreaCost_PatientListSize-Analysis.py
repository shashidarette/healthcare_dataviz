
# coding: utf-8

# # This notebook is to analyse and discover relation between prescription costs of a practice against its patient list size.
# ## As part of the analysis - latest datasets of Dec 2017 are considered for both. The primary focus is whether the patient list can be used to correlate with the cost.

# In[4]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ## Area Q59 prescription cost versus patient list size analysis

# In[2]:


# Presctiption Cost (filter from actual prescription cost data for Dec 17)
Q59PrescrptionData = pd.read_csv('./Q59_Costs.csv', sep=',', encoding = "ISO-8859-1")
Q59PrescrptionData.head()


# In[3]:


# Patient list size (filter from actual patient list size data for Oct-Dec 17)
Q59PatientSizeData = pd.read_csv('./Q59_PatientListSizes.csv', sep=',', encoding = "ISO-8859-1")
Q59PatientSizeData.head()


# In[4]:


Q59PatientSlice = Q59PatientSizeData.loc[:, 'Practice Code':]


# In[5]:


# Merge both prescription and patient list size data for Q59
Q59MergedData = Q59PrescrptionData.merge(Q59PatientSlice, left_on='PRACTICE', right_on='Practice Code', how='inner')
Q59MergedData.head()


# ## Scatter plot of patient list vs cost with regression

# In[6]:


x = Q59MergedData['TotalSize']
y = Q59MergedData['ACT COST   ']
s = Q59MergedData['ACT COST   '].count() * 10 + Q59MergedData['ACT COST   '].max() + 100
ax = plt.gca()
ax.grid(True)
plt.scatter(x, y)
plt.xlabel("Practice Size")
plt.ylabel("Practice total cost")
sns.regplot(x='TotalSize', y='ACT COST   ', data=Q59MergedData)
plt.show()


# ### From the above graph its evident that they are practices which have higher or lower cost in comparision to regression line. These practices are of interest of the differences.

# ## Prescription cost vs Patient list size comparision at UK level
# ### The datasets are generated from the main datasets

# In[5]:


# Prescription cost at UK level
UKPrescrptionCosts = pd.read_csv('./UK_PracticeCosts.csv', sep=',', encoding = "ISO-8859-1")
UKPrescrptionCosts.head()


# In[6]:


# Practice lists at UK level
UKPracticeListTotals = pd.read_csv('./UK_PracticeListSize.csv', sep=',', encoding = "ISO-8859-1")
UKPracticeListTotals.head()


# ### Merge the data of costs and patient list

# In[7]:


UKMergedData = UKPrescrptionCosts.merge(UKPracticeListTotals, left_on='PRACTICE', right_on='Practice Code', how='inner')
UKMergedData.head()


# ## Scatter plot of patient list vs cost with regression at UK level

# In[8]:


maxSize = UKMergedData['TotalSize'].max()
maxCost = UKMergedData['ACT COST   '].max()
x = UKMergedData['TotalSize']
y = UKMergedData['ACT COST   ']
s = maxCost * 10 + 100

ax = plt.gca()
ax.grid(True)

plt.scatter(x, y)
plt.xlabel("Practice Size")
plt.ylabel("Practice total cost")

sns.regplot(x='TotalSize', y='ACT COST   ', data=UKMergedData)

plt.show()


# ### From the above graph its evident that they are practices which have higher or lower cost in comparision to regression line. These practices are of interest of the differences.
# ### Specifically the number of practices of patient list between 0-10000 and 10000-~26500 are of interest.

# In[9]:


UKMergedData.describe()


# ### Based on the distribution of data, total number of practices are consideration is 7628.
# ### To decrease the data size, lets consider practices between 25% and 75% i.e. patient list between 4400 & 10600.
# ### The number of practices reduces to 1812

# In[10]:


# Consider patient list size between 25% to 75% percentile
Percent25 = 4400
Percent75 = 10600
PatientSizeFilter1 = UKMergedData['TotalSize'] >= Percent25
PatientSizeFilter2 = UKMergedData['TotalSize'] <= Percent75
PatientSizeFilterData = UKMergedData[PatientSizeFilter1 & PatientSizeFilter2]
PatientSizeFilterData.head()


# ## Scatter plot of patient list vs cost with regression (25% to 75% percentiles)

# In[11]:


maxSize = PatientSizeFilterData['TotalSize'].max()
maxCost = PatientSizeFilterData['ACT COST   '].max()

sns.jointplot(x="TotalSize", y="ACT COST   ", data=PatientSizeFilterData, kind='reg',
                  joint_kws={'line_kws':{'color':'cyan'}})
print(PatientSizeFilterData.shape)
plt.show()


# ## Above graph validates the understanding that practices of size between 4400 & 10600 have higher difference in costs. Further analysis needs to be done to understand the reasons for these differences.

# In[12]:


UKMergedData['PerPatient_NIC'] = UKMergedData['NIC        ']/UKMergedData['TotalSize']
UKMergedData['PerPatient_ActCost'] = UKMergedData['ACT COST   ']/UKMergedData['TotalSize']


# In[13]:


# Scatter plot of per-patient act cost for UK

x = np.arange(0, UKMergedData['ACT COST   '].count(), 1.0)
y = UKMergedData['ACT COST   ']

plt.scatter(x, y)
plt.xlabel("Practice Index")
plt.ylabel("Total Act cost")
plt.show()


# In[14]:


# Scatter plot of per-patient act cost for UK

x = np.arange(0, UKMergedData['PerPatient_ActCost'].count(), 1.0)
y = UKMergedData['PerPatient_ActCost']

plt.scatter(x, y)
plt.xlabel("Practice Index")
plt.ylabel("Per patient cost")
plt.show()


# In[16]:


# Scatter plot of per-patient act cost for UK
PerPFilter = UKMergedData['PerPatient_ActCost'] < 500

PerPFilter25 = UKMergedData['TotalSize'] >= Percent25
PerPFilter75 = UKMergedData['TotalSize'] <= Percent75

PerPFilterData = UKMergedData[PerPFilter & PerPFilter25 & PerPFilter75]
x = PerPFilterData['TotalSize'] #np.arange(0, UKMergedData['PerPatient_ActCost'].count(), 1.0)
y = PerPFilterData['PerPatient_ActCost']

plt.scatter(x, y)
plt.xlabel("Practice Index")
plt.ylabel("Per patient cost")
plt.show()


# In[21]:


UKMergedData['PerPatient_ActCost'].describe()

