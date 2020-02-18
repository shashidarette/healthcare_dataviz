
# coding: utf-8

# ## This notebook is to analyse the practice indicators available from PHE dataset

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


# General Practice Indicators from PHE (It includes England, CCG level indicators as well)
GPIndicators = pd.read_csv('..\..\..\..\MAIN_PROJECT\Data\PHE\PracticeProfileIndicators.csv', sep=',', encoding = "ISO-8859-1")
GPIndicators.head()


# In[3]:


GPIndicators.columns


# In[4]:


# types of areas
GPIndicators['Area Type'].unique()


# In[9]:


# types of indicators data available
GPIndicators['Indicator Name'].unique()


# In[10]:


# types of indicators data available
GPIndicators['Indicator ID'].unique()


# In[7]:


# Time periods avaoilable
GPIndicators['Time period'].unique()


# In[26]:


# AreaTypeFilters
GPFilter = GPIndicators['Area Type'] == 'GP'
CCGFilter = GPIndicators['Area Type'] == 'CCGs (since 4/2017)'
EnglandFilter = GPIndicators['Area Type'] == 'Country'


# In[27]:


# Data by AreaType
GP_Data = GPIndicators[GPFilter]
CCG_Data = GPIndicators[CCGFilter]
England_Data = GPIndicators[EnglandFilter]


# In[28]:


# Save to CSV
GP_Data.to_csv('PHE_GP_Indicators.csv', sep=',')


# In[29]:


# Save to CSV
CCG_Data.to_csv('PHE_CCG_Indicators.csv', sep=',')


# In[30]:


# Save to CSV
England_Data.to_csv('PHE_ENG_Indicators.csv', sep=',')


# In[36]:


# Extract IMD 2015 data from GP Data
GP_IMD_2k15_Filter = GP_Data['Indicator Name'] == 'Deprivation score (IMD 2015)' 
GP_IMD_2k15_Data = GP_Data[GP_IMD_2k15_Filter]
GP_IMD_2k15_Data.to_csv('PHE_GP_IMD_2k15_Indicators.csv', sep=',')


# In[49]:


# Scatter plot of per-patient act cost for UK
IMDColumnFilter = GP_IMD_2k15_Data['Indicator Name'] == 'Deprivation score (IMD 2015)' 
IMDData = GP_IMD_2k15_Data[IMDColumnFilter]
x = np.arange(0, IMDData['Indicator Name'].count(), 1)
y = IMDData['Value']

plt.scatter(x, y)
plt.xlabel("Practice Index")
plt.ylabel("IMD Score")
plt.show()

