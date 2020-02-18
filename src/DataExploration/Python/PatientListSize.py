
# coding: utf-8

# ## This notebooks deals the patient list size data exploration##
# # User can choose the area code and compare its mean with overall UK mean patient list size #

# In[3]:


import pandas as pd
patient_list = pd.read_csv('Patient_List_Size_Dec17.csv', sep=',', encoding = "ISO-8859-1")


# In[4]:


patient_list.columns


# In[5]:


patient_list.head()


# In[6]:


# patient_list[['Male 0-4'],['Female 0-4'], ['Male 5-14'], ['Female 5-14'],
#       ['Male 15-24'], ['Female 15-24'], ['Male 25-34'], ['Female 25-34'],
#       ['Male 35-44'], ['Female 35-44'], ['Male 45-54'], ['Female 45-54'],
#       ['Male 55-64'], ['Female 55-64'], ['Male 65-74'], ['Female 65-74'], ['Male 75+'],
#       ['Female 75+']]
patient_list['TotalSize'] = patient_list['Male 0-4']+ patient_list['Female 0-4'] + patient_list ['Male 5-14']+ patient_list['Female 5-14']+patient_list['Male 15-24']+patient_list['Female 15-24']+ patient_list['Male 25-34']+patient_list['Female 25-34']+patient_list['Male 35-44']+ patient_list['Female 35-44']+ patient_list['Male 45-54']+ patient_list['Female 45-54']+ patient_list['Male 55-64']+ patient_list['Female 55-64']+ patient_list['Male 65-74']+ patient_list['Female 65-74']+ patient_list['Male 75+']+ patient_list['Female 75+']
patient_list['TotalSize'].describe()


# In[39]:


patient_list.head()


# In[40]:


patient_list['Area Team Code'].unique()


# In[41]:


## SELECT AREA CODE FROM ABOVE
AreaCode = 'Q59'


# In[42]:


# CREATE AND APPLY AREA FILTER BASED ON AREA CODE
AreaFilter = patient_list['Area Team Code'] == AreaCode
AreaPatientList = patient_list[AreaFilter]
AreaPatientList.describe()


# In[43]:


AreaMean = AreaPatientList.mean()
PatientListMean = patient_list.mean()

print(AreaMean)
print(PatientListMean)


# In[44]:


# Drop TotalSize if computed
#AreaMean = AreaMean.drop(['TotalSize'])
#PatientListMean = PatientListMean.drop(['TotalSize'])


# In[45]:


#referred : https://matplotlib.org/gallery/statistics/barchart_demo.html
import numpy as np
import matplotlib.pyplot as plt

n_groups = len(AreaMean.index)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}


rects1 = ax.bar(index, AreaMean.values, bar_width,
                alpha=opacity, color='b',
                error_kw=error_config,
                label=AreaCode)

rects2 = ax.bar(index + bar_width, PatientListMean.values, bar_width,
                alpha=opacity, color='r',
                error_kw=error_config,
                label='UK')

ax.set_xlabel('Age group')
ax.set_ylabel('Participant size')
ax.set_title(AreaCode + ' vs UK')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(AreaMean.index.values, rotation=90)
ax.legend()

fig.tight_layout()
plt.show()


# In[46]:


practiceCodeFilter = patient_list['Practice Code'] == 'C82005'
practice = patient_list[practiceCodeFilter]
#print(len(practice.columns))
ageGroupsData = practice[practice.columns[8:]]
ageGroupsData.values


# In[47]:


PracticeCode1 = 'C83079'
PracticeCode2 = 'C83633'

# Filters
practiceCodeFilter1 = patient_list['Practice Code'] == PracticeCode1
practiceCodeFilter2 = patient_list['Practice Code'] == PracticeCode2

practice1 = patient_list[practiceCodeFilter1]
practice2 = patient_list[practiceCodeFilter2]

# Drop TotalSize if computed
#practice1 = practice1.drop(['TotalSize'])
#practice2 = practice2.drop(['TotalSize'])

print(practice1[practice.columns[8:]].values[0])
print(practice2[practice.columns[8:]].values[0])




# In[59]:


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


rects1 = ax.bar(index, practice1[practice.columns[8:]].values[0], bar_width,
                alpha=opacity, color='b',
                error_kw=error_config,
                label= PracticeCode1)

rects2 = ax.bar(index + bar_width, practice2[practice.columns[8:]].values[0], bar_width,
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
ax.set_xticklabels(practice.columns[8:], rotation=90)
ax.legend()

fig.tight_layout()
plt.show()


# In[16]:


# Fixing random state for reproducibility
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, patient_list['TotalSize'].count(), 1.0)
y = patient_list['TotalSize']
s = patient_list['TotalSize'].count() * 10 + patient_list['TotalSize'].max() + 100

plt.scatter(x, y)
plt.xlabel("Practice Index")
plt.ylabel("Patient List Size")
plt.show()


# In[20]:


#patient_list['TotalSize']
import seaborn as sns
sns.set(color_codes=True)
sns.distplot(patient_list['TotalSize']);
plt.show()


# In[21]:


AreaCodeFilter = patient_list['Area Team Code'] == 'Q59'
AreaCodePractices = patient_list[AreaCodeFilter]
AreaCodePractices.head()


# In[22]:


# Fixing random state for reproducibility
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, AreaCodePractices['TotalSize'].count(), 1.0)
y = AreaCodePractices['TotalSize']
s = AreaCodePractices['TotalSize'].count() * 10 + AreaCodePractices['TotalSize'].max() + 100

plt.scatter(x, y)
plt.xlabel("Practice Index")
plt.ylabel("Patient List Size")
plt.show()


# In[23]:


AreaCodePractices.describe()


# In[24]:


import seaborn as sns
sns.set(color_codes=True)
sns.distplot(AreaCodePractices['TotalSize']);
plt.show()


# In[27]:


AreaCodePractices.to_csv("Q59_PatientListSizes.csv", sep=',')

