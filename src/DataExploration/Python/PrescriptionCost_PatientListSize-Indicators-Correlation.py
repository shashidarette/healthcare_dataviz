
# coding: utf-8

# # This notebook is to analyse and discover relation between prescription costs of a practice against its patient list size.
# ## As part of the analysis - latest datasets of Dec 2017 are considered for both. The primary focus is whether the patient list can be used to correlate with the cost.

# In[2]:


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

# In[10]:


# Prescription cost at UK level
UKPrescrptionCosts = pd.read_csv('./UK_PracticeCosts.csv', sep=',', encoding = "ISO-8859-1")
UKPrescrptionCosts.head()


# In[11]:


# Practice lists at UK level
UKPracticeListTotals = pd.read_csv('./UK_PracticeListSize.csv', sep=',', encoding = "ISO-8859-1")
UKPracticeListTotals.head()


# ### Merge the data of costs and patient list

# In[12]:


UKMergedData = UKPrescrptionCosts.merge(UKPracticeListTotals, left_on='PRACTICE', right_on='Practice Code', how='inner')
UKMergedData.head()


# ## Scatter plot of patient list vs cost with regression at UK level

# In[13]:


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

# In[14]:


UKMergedData.describe()


# ### Based on the distribution of data, total number of practices are consideration is 7628.
# ### To decrease the data size, lets consider practices between 25% and 75% i.e. patient list between 4400 & 10600.
# ### The number of practices reduces to 1812

# In[15]:


# Consider patient list size between 25% to 75% percentile
Percent25 = 4400
Percent75 = 10600
PatientSizeFilter1 = UKMergedData['TotalSize'] >= Percent25
PatientSizeFilter2 = UKMergedData['TotalSize'] <= Percent75
PatientSizeFilterData = UKMergedData[PatientSizeFilter1 & PatientSizeFilter2]
PatientSizeFilterData.head()


# ## Scatter plot of patient list vs cost with regression (25% to 75% percentiles)

# In[16]:


maxSize = PatientSizeFilterData['TotalSize'].max()
maxCost = PatientSizeFilterData['ACT COST   '].max()

sns.jointplot(x="TotalSize", y="ACT COST   ", data=PatientSizeFilterData, kind='reg',
                  joint_kws={'line_kws':{'color':'cyan'}})
print(PatientSizeFilterData.shape)
plt.show()


# ## Above graph validates the understanding that practices of size between 4400 & 10600 have higher difference in costs. Further analysis needs to be done to understand the reasons for these differences.

# In[17]:


UKMergedData['PerPatient_NIC'] = UKMergedData['NIC        ']/UKMergedData['TotalSize']
UKMergedData['PerPatient_ActCost'] = UKMergedData['ACT COST   ']/UKMergedData['TotalSize']


# In[18]:


# Scatter plot of per-patient act cost for UK

x = np.arange(0, UKMergedData['ACT COST   '].count(), 1.0)
y = UKMergedData['ACT COST   ']

plt.scatter(x, y)
plt.xlabel("Practice Index")
plt.ylabel("Total Act cost")
plt.show()


# In[19]:


# Scatter plot of per-patient act cost for UK

x = np.arange(0, UKMergedData['PerPatient_ActCost'].count(), 1.0)
y = UKMergedData['PerPatient_ActCost']

plt.scatter(x, y)
plt.xlabel("Practice Index")
plt.ylabel("Per patient cost")
plt.show()


# In[20]:


# Define filters for per-patient act cost for UK
PerPFilter = UKMergedData['PerPatient_ActCost'] < 500

PerPFilter25 = UKMergedData['TotalSize'] >= Percent25
PerPFilter75 = UKMergedData['TotalSize'] <= Percent75

PerPFilterData = UKMergedData[PerPFilter & PerPFilter25 & PerPFilter75]


# In[21]:


# Scatter plot of per-patient act cost for UK
x = PerPFilterData['TotalSize'] #np.arange(0, UKMergedData['PerPatient_ActCost'].count(), 1.0)
y = PerPFilterData['PerPatient_ActCost']

plt.scatter(x, y)
plt.xlabel("Practice Index")
plt.ylabel("Per patient cost")
plt.show()


# In[22]:


UKMergedData['PerPatient_ActCost'].describe()


# In[23]:


# Load all GP Indicators
GP_Indicators = pd.read_csv('./PHE_GP_Indicators.csv', sep=',', encoding = "ISO-8859-1")


# In[24]:


GP_Indicators.columns


# In[25]:


GP_Indicators['Time period'].unique()


# In[26]:


# GP_Indicators filters
GPFilter = GP_Indicators['Area Type'] == 'GP'
GP_IMD_2k15_Filter = GP_Indicators['Indicator Name'] == 'Deprivation score (IMD 2015)' 
GP_65Plus_Filter = GP_Indicators['Indicator Name'] ==  '% aged 65+ years'


# In[27]:


GP_65Plus_Data = GP_Indicators[GP_65Plus_Filter]
GP_IMD_2k15_Data = GP_Indicators[GP_IMD_2k15_Filter]


# In[28]:


GP_65PlusData_2017Filter = GP_65Plus_Data['Time period'] == 2017


# In[29]:


GP_65Plus_Data_2017 = GP_65Plus_Data[GP_65PlusData_2017Filter]


# In[30]:


GP_65Plus_Data_2017.shape


# In[31]:


Features = ['Area Code', 'Indicator Name', 'Value']
GP_65Plus_Selected = GP_65Plus_Data_2017[Features]
GP_IMD_2k15_Selected = GP_IMD_2k15_Data[Features]


# In[32]:


GP_65Plus_Selected.to_csv("GP_65Plus_Data.csv", sep=',')


# ## PHE Diabetes indicators

# In[33]:


# Import diabetes indicators data
diabeticIndicatorsData = pd.read_csv('..\..\..\..\MAIN_PROJECT\Data\PHE\DiabetesProfileIndicators.csv', sep=',', encoding = "ISO-8859-1")


# In[34]:


selectedFeatures = ['Area Code', 'Indicator ID', 'Indicator Name', 'Time period', 'Count']


# In[35]:



diabeticIndicatorsSelectedData = diabeticIndicatorsData[selectedFeatures]


# In[36]:


IndicatorFilter = diabeticIndicatorsSelectedData['Indicator ID'] == 241
TimePeriodFilter = diabeticIndicatorsSelectedData['Time period'] == '2016/17'


# In[37]:


diabeticIndicators2017 = diabeticIndicatorsSelectedData[IndicatorFilter & TimePeriodFilter]


# In[38]:


diabeticIndicators2017.head


# In[3]:


# Import CVD indicators data
cvdIndicatorsData = pd.read_csv('..\..\..\..\MAIN_PROJECT\Data\PHE\CVD-RiskfactorsforCVD.Data.csv', sep=',', encoding = "ISO-8859-1")


# In[4]:


cvdIndicatorFilter = cvdIndicatorsData['Indicator ID'] == 219
cvdTimePeriodFilter = cvdIndicatorsData['Time period'] == '2016/17'


# In[6]:


cvdIndicators2017 = cvdIndicatorsData[cvdIndicatorFilter & cvdTimePeriodFilter]


# In[9]:


cvdIndicatorsSelectedData = cvdIndicators2017[selectedFeatures]


# In[39]:


UKMergedDataSelected = UKMergedData.merge(GP_65Plus_Selected, left_on='PRACTICE', right_on='Area Code', how='inner')
UKMergedDataSelected = UKMergedDataSelected.merge(diabeticIndicators2017, left_on='PRACTICE', right_on='Area Code', how='inner')
UKMergedDataSelected = UKMergedDataSelected.merge(cvdIndicatorsSelectedData, left_on='PRACTICE', right_on='Area Code', how='inner')
UKMergedDataSelected = UKMergedDataSelected.merge(GP_IMD_2k15_Selected, left_on='PRACTICE', right_on='Area Code', how='inner')
UKMergedDataSelected.describe()
UKMergedDataSelected.head


# In[40]:


UKMergedDataSelected.columns


# In[41]:


UKMergedDataSelected.to_csv("UKMergedDataSelected.csv", sep=',')


# In[23]:


# IMD indicators for GP from PHE
#GP_IMD2k15 = pd.read_csv('./PHE_GP_IMD_2k15_Indicators.csv', sep=',', encoding = "ISO-8859-1")
#GP_IMD2k15.head()


# In[24]:


UKMergedDataWithIMD = UKMergedData.merge(GP_IMD2k15, left_on='PRACTICE', right_on='Area Code', how='inner')
UKMergedDataWithIMD.describe()


# In[25]:


# Scatter plot of per-patient act cost for UK
x = UKMergedDataWithIMD['PerPatient_ActCost'] #np.arange(0, UKMergedData['PerPatient_ActCost'].count(), 1.0)
y = UKMergedDataWithIMD['Value']

plt.scatter(x, y)
plt.xlabel("Per patient cost")
plt.ylabel("IMD")
plt.show()


# In[26]:


PerPFilter_IMD = UKMergedDataWithIMD['PerPatient_ActCost'] < 500
PerPFilter25_IMD = UKMergedDataWithIMD['TotalSize'] >= Percent25
PerPFilter75_IMD = UKMergedDataWithIMD['TotalSize'] <= Percent75
PerPFilterDataWithIMD = UKMergedDataWithIMD[PerPFilter_IMD & PerPFilter25_IMD & PerPFilter75_IMD]


# In[27]:


# Scatter plot of per-patient act cost for UK between 25% and 75%
x = PerPFilterDataWithIMD['TotalSize'] #np.arange(0, UKMergedData['PerPatient_ActCost'].count(), 1.0)
y = PerPFilterDataWithIMD['Value']

plt.scatter(x, y)
plt.xlabel("Per patient cost")
plt.ylabel("IMD")
plt.show()


# In[29]:


# Scatter plot of IMD against age profile
x = PerPFilterDataWithIMD['AvgAgeProfile'] #np.arange(0, UKMergedData['PerPatient_ActCost'].count(), 1.0)
y = PerPFilterDataWithIMD['PerPatient_ActCost']

plt.scatter(x, y)
plt.xlabel("Average Age")
plt.ylabel("IMD")
plt.show()


# In[21]:


PerPFilterDataWithIMD.columns


# In[31]:


from mpl_toolkits.mplot3d import Axes3D


# In[34]:


threedee = plt.figure().gca(projection='3d')
threedee.scatter(UKMergedDataWithIMD['AvgAgeProfile'], UKMergedDataWithIMD['PerPatient_ActCost'], UKMergedDataWithIMD['Value'])
threedee.set_xlabel('AvgAgeProfile')
threedee.set_ylabel('IMD')
threedee.set_zlabel('Per patient cost')
plt.show()


# In[ ]:


threedee = plt.figure().gca(projection='3d')
threedee.scatter(PerPFilterDataWithIMD['TotalSize'], PerPFilterDataWithIMD['PerPatient_ActCost'], PerPFilterDataWithIMD['Value'])
threedee.set_xlabel('TotalSize')
threedee.set_ylabel('IMD')
threedee.set_zlabel('Per patient cost')
plt.show()


# #reference : https://plot.ly/pandas/3d-scatter-plots/
# import plotly.plotly as py
# import plotly.graph_objs as go
# import pandas as pd
# 
# data = []
# clusters = []
# colors = ['rgb(228,26,28)','rgb(55,126,184)','rgb(77,175,74)']
# 
# for i in range(len(PerPFilterDataWithIMD['PRACTICE'].unique())):
#     name = PerPFilterDataWithIMD['PRACTICE'].unique()[i]
#     x = PerPFilterDataWithIMD[PerPFilterDataWithIMD['PRACTICE'] == name]['Value']
#     y = PerPFilterDataWithIMD[PerPFilterDataWithIMD['PRACTICE'] == name]['PerPatient_ActCost']
#     z = PerPFilterDataWithIMD[PerPFilterDataWithIMD['PRACTICE'] == name]['TotalSize']
#     
#     trace = dict(
#         name = name,
#         x = x, y = y, z = z,
#         type = "scatter3d",    
#         mode = 'markers',
#         marker = dict( size=3, line=dict(width=0) ) )
#     data.append( trace )
# 
# layout = dict(
#     width=800,
#     height=550,
#     autosize=False,
#     title='Dataset correlation',
#     scene=dict(
#         xaxis=dict(
#             gridcolor='rgb(255, 255, 255)',
#             zerolinecolor='rgb(255, 255, 255)',
#             showbackground=True,
#             backgroundcolor='rgb(230, 230,230)'
#         ),
#         yaxis=dict(
#             gridcolor='rgb(255, 255, 255)',
#             zerolinecolor='rgb(255, 255, 255)',
#             showbackground=True,
#             backgroundcolor='rgb(230, 230,230)'
#         ),
#         zaxis=dict(
#             gridcolor='rgb(255, 255, 255)',
#             zerolinecolor='rgb(255, 255, 255)',
#             showbackground=True,
#             backgroundcolor='rgb(230, 230,230)'
#         ),
#         aspectratio = dict( x=1, y=1, z=0.7 ),
#         aspectmode = 'manual'        
#     ),
# )
# 
# fig = dict(data=data, layout=layout)
# 
# # IPython notebook
# #py.iplot(fig, filename='pandas-3d-iris', validate=False)
# 
# url = py.plot(fig, filename='pandas-3d-correlation', validate=False)

# In[43]:


from IPython.display import Image
Image("insights/GP_Costs_vs_TotalSize_sample.png")


# In[54]:


PracticeCode1 = 'F81741' #'C83079''C83064'#
PracticeCode2 = 'M92035'#'C83633''C83007'#
P1Filter = PerPFilterDataWithIMD['PRACTICE'] == PracticeCode1
P2Filter = PerPFilterDataWithIMD['PRACTICE'] == PracticeCode2
P1Data = PerPFilterDataWithIMD[P1Filter]
P2Data = PerPFilterDataWithIMD[P2Filter]


# In[56]:


# VIEW PRACTICE AGE GROUPS SIDE BY SIDE
#referred : https://matplotlib.org/gallery/statistics/barchart_demo.html

import numpy as np
import matplotlib.pyplot as plt

n_groups = 18

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}


rects1 = ax.bar(index, P1Data[P1Data.columns[15:33]].values[0], bar_width,
                alpha=opacity, color='b',
                error_kw=error_config,
                label= PracticeCode1)

rects2 = ax.bar(index + bar_width, P2Data[P2Data.columns[15:33]].values[0], bar_width,
                alpha=opacity, color='r',
                error_kw=error_config,
                label= PracticeCode2)

#rects3 = ax.bar(index + bar_width * 2, AreaMean.values, bar_width,
#                alpha=opacity, color='g',
#                error_kw=error_config,
#                label= 'UK')

ax.set_xlabel('Age group')
ax.set_ylabel('Participant size')
ax.set_title(PracticeCode1 + ' vs ' + PracticeCode2) #  + ' vs ' + 'UK')
ax.set_xticks(index + bar_width)
ax.set_xticklabels(P1Data.columns[15:33], rotation=90)
ax.legend()

fig.tight_layout()
plt.show()


# In[45]:


PerPFilterDataWithIMD.columns


# In[53]:


P2Data[P2Data.columns[15:33]].values[0]


# In[35]:


UKMergedDataWithIMD.columns


# In[36]:


UKMergedDataWithIMD.drop(['PERIOD', 'Unnamed: 0_x', 'Regional Office Name', 'Regional Office Code',  'Unnamed: 0_y', 'Time period', 'Lower CI 95.0 limit', 'Upper CI 95.0 limit', 'Lower CI 99.8 limit', 'Upper CI 99.8 limit', 'Time period Sortable'], axis=1, inplace=True)


# In[37]:


UKMergedDataWithIMD.to_csv("UKMergedDataWithIMD.csv", sep=',')

