
# coding: utf-8

# # This notebook combines 3 datasets to discover correlation between them. They are as below:
# #    - Practice Prescription data for Dec 17 (NHS Digital)
# #    - Patient list size from Oct-Dec17 Quarter (NHS BSA)
# #    - Diabetics Indicators (latest - 2016/17) (PHE)
# #    - CVD-Riskfactors Indicators (latest data) (PHE)

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[8]:


# Import practice prescription data
prescriptionData = pd.read_csv('./T201712PDPI+BNFT.CSV', sep=',', encoding = "ISO-8859-1")
prescriptionData['CHAPTER'] = prescriptionData['BNF CODE'].str[:2]
prescriptionData.head()


# In[2]:


# Import patient list size data
patientListSizeData = pd.read_csv('Patient_List_Size_Dec17.csv', sep=',', encoding = "ISO-8859-1")
patientListSizeData.head()


# In[3]:


# Import diabetes indicators data
diabeticIndicatorsData = pd.read_csv('..\..\..\..\MAIN_PROJECT\Data\PHE\DiabetesProfileIndicators.csv', sep=',', encoding = "ISO-8859-1")
#print(diabeticIndicatorsData.head(15))


# In[4]:


# Import cvd indicators data
cvdIndicatorsData = pd.read_csv('..\..\..\..\MAIN_PROJECT\Data\PHE\CVD-RiskfactorsforCVD.Data.csv', sep=',', encoding = "ISO-8859-1")
#print(cvdIndicatorsData.head(15))


# In[81]:


# Initialize base analysis parameters - practice codes and Chapter
PracticeCode1 = 'C83064'#'F81741' #'C83079'
PracticeCode2 = 'B81008'#'G82090' 'C83007'#'M92035'#'C83633'
Chapter       = '06'


# In[82]:


# Prescription Data comparision between two practices
# Data Filters
PracticeFilter1 = prescriptionData['PRACTICE'] == PracticeCode1
PracticeFilter2 = prescriptionData['PRACTICE'] == PracticeCode2
ChapterFilter = prescriptionData['CHAPTER'] ==  Chapter


# In[83]:


# Practice 1
PracticeData1 = prescriptionData[PracticeFilter1]
PracticeData1ByChapter = PracticeData1.groupby('CHAPTER')
PracticeData1ByChapter.sum()


# In[84]:


# Practice 2
PracticeData2 = prescriptionData[PracticeFilter2]
PracticeData2ByChapter = PracticeData2.groupby('CHAPTER')
PracticeData2ByChapter.sum()


# In[87]:


# Patient List Size data comparision between two practices
patientSizeFilter1 = patientListSizeData['Practice Code'] == PracticeCode1
patientSizeFilter2 = patientListSizeData['Practice Code'] == PracticeCode2

practice1 = patientListSizeData[patientSizeFilter1]
practice2 = patientListSizeData[patientSizeFilter2]


# In[88]:



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

practice1Values = practice1[practice1.columns[8:]].values[0]
practice2Values = practice2[practice1.columns[8:]].values[0]

print(PracticeCode1 + ': ' + str(practice1Values.sum()))
print(PracticeCode2 + ': ' + str(practice2Values.sum()))

rects1 = ax.bar(index, practice1Values, bar_width,
                alpha=opacity, color='b',
                error_kw=error_config,
                label= PracticeCode1)

rects2 = ax.bar(index + bar_width, practice2Values, bar_width,
                alpha=opacity, color='r',
                error_kw=error_config,
                label= PracticeCode2)

ax.set_xlabel('Age group')
ax.set_ylabel('Participant size')
ax.set_title(PracticeCode1 + ' vs ' + PracticeCode2) #  + ' vs ' + 'UK')
ax.set_xticks(index + bar_width)
ax.set_xticklabels(practice1.columns[8:], rotation=90)
ax.legend()

fig.tight_layout()
plt.show()


# In[79]:


# Diabetic indicator comparision between two practices
IndicatorFilter = diabeticIndicatorsData['Indicator ID'] == 241
TimePeriodFilter = diabeticIndicatorsData['Time period'] == '2016/17'

AreaCodeFilter1 = diabeticIndicatorsData['Area Code'] == PracticeCode1
AreaCodeFilter2 = diabeticIndicatorsData['Area Code'] == PracticeCode2

Practice1DbIndi = diabeticIndicatorsData[IndicatorFilter & AreaCodeFilter1 & TimePeriodFilter]
Practice2DbIndi = diabeticIndicatorsData[IndicatorFilter & AreaCodeFilter2 & TimePeriodFilter]

print(str(Practice1DbIndi['Count'].values) + ' vs ' + str(Practice2DbIndi['Count'].values))


# In[80]:


# CVD indicator comparision between two practices
CvdIndicatorFilter = cvdIndicatorsData['Indicator ID'] == 219
AreaCodeFilter1 = cvdIndicatorsData['Area Code'] == PracticeCode1
AreaCodeFilter2 = cvdIndicatorsData['Area Code'] == PracticeCode2

Practice1CvdIndi = cvdIndicatorsData[CvdIndicatorFilter & AreaCodeFilter1 & TimePeriodFilter]
Practice2CvdIndi = cvdIndicatorsData[CvdIndicatorFilter & AreaCodeFilter2 & TimePeriodFilter]

print(str(Practice1CvdIndi['Count'].values) + ' vs ' + str(Practice2CvdIndi['Count'].values))


# In[15]:


PrescriptionByPractice = prescriptionData.groupby('PRACTICE')
#PrescriptionByPractice.describe()


# In[25]:


AreaCodeFilter = prescriptionData[' SHA'] == 'Q59'
AreaCodeQ59 = prescriptionData[AreaCodeFilter]


# In[26]:


PrescriptionQ59ByPractice = AreaCodeQ59.groupby('PRACTICE')
#PrescriptionQ59ByPractice.head()


# In[9]:


PrescriptionQ59ByPracticeSUM = PrescriptionQ59ByPractice.sum()


# In[10]:


PrescriptionQ59ByPracticeSUM.columns


# In[11]:


import seaborn as sns
sns.set(color_codes=True)
sns.distplot(PrescriptionQ59ByPracticeSUM['ACT COST   ']);
plt.show()


# In[12]:


# Scatter plot of total practice costs for Q59 area
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, PrescriptionQ59ByPracticeSUM['ACT COST   '].count(), 1.0)
y = PrescriptionQ59ByPracticeSUM['ACT COST   ']
s = PrescriptionQ59ByPracticeSUM['ACT COST   '].count() * 10 + PrescriptionQ59ByPracticeSUM['ACT COST   '].max() + 100

plt.scatter(x, y)
plt.xlabel("Practice Index")
plt.ylabel("Practice total cost")
plt.show()


# In[13]:


PrescriptionQ59ByPracticeSUM.to_csv("Q59_Costs.csv", sep=',')


# In[17]:


PrescriptionByPracticeCosts = PrescriptionByPractice.sum()


# In[3]:


patientListSizeData['TotalSize'] = patientListSizeData['Male 0-4'] + patientListSizeData['Female 0-4'] + patientListSizeData['Male 5-14']+ patientListSizeData['Female 5-14']+patientListSizeData['Male 15-24']+patientListSizeData['Female 15-24']+ patientListSizeData['Male 25-34']+patientListSizeData['Female 25-34']+patientListSizeData['Male 35-44']+ patientListSizeData['Female 35-44']+ patientListSizeData['Male 45-54']+ patientListSizeData['Female 45-54']+ patientListSizeData['Male 55-64']+ patientListSizeData['Female 55-64']+ patientListSizeData['Male 65-74']+ patientListSizeData['Female 65-74']+ patientListSizeData['Male 75+']+ patientListSizeData['Female 75+']
patientListSizeData.head()


# In[4]:


# To find the average age profile of a GP
patientListSizeData['AvgAgeProfile'] = (patientListSizeData['Male 0-4'] *4 + patientListSizeData['Female 0-4'] * 4 + patientListSizeData['Male 5-14'] * 14 + patientListSizeData['Female 5-14'] * 14 +patientListSizeData['Male 15-24'] * 24 +patientListSizeData['Female 15-24'] * 24  + patientListSizeData['Male 25-34'] * 34 +patientListSizeData['Female 25-34'] * 34 +patientListSizeData['Male 35-44'] * 44 + patientListSizeData['Female 35-44'] * 44 + patientListSizeData['Male 45-54'] * 54 + patientListSizeData['Female 45-54'] * 54 + patientListSizeData['Male 55-64'] * 64+ patientListSizeData['Female 55-64'] * 64 + patientListSizeData['Male 65-74'] * 74+ patientListSizeData['Female 65-74'] * 74 + patientListSizeData['Male 75+'] * 100 + patientListSizeData['Female 75+'] * 100) / patientListSizeData['TotalSize']
patientListSizeData['AvgAgeProfile'].describe()


# In[32]:


#PrescriptionByPracticeCosts.to_csv("UK_PracticeCosts.csv", sep=',')


# In[6]:


patientListSizeData.to_csv("UK_PracticeListSize.csv", sep=',')


# In[41]:


practice2[practice1.columns[8:]].values[0].sum()


# In[89]:


prescriptionData['ACT COST   '].describe()

