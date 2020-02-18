
# coding: utf-8

# # This notebook is used to explore the Practice level prescription data from NHS Digital for the montrh of Dec 2017
# 

# In[1]:


import pandas as pd
presDec17 = pd.read_csv('./T201712PDPI+BNFT.CSV', sep=',', encoding = "ISO-8859-1")
print(type(presDec17))
presDec17.head(15)


# In[2]:


presDec17.describe()


# In[3]:


# UPDATE CHAPTER NUMBER - 2 characters of BNF CODE
presDec17['CHAPTER'] = presDec17['BNF CODE'].str[:2]
presDec17.head()


# In[36]:


# CONSIDER A SPECIFIC CHAPTER OF PRESCRIPTIONS : 06 => Endocrine System (includes Diabetic Medicines)
ChapterFilter = presDec17['CHAPTER'] == '06'
ChapterData = presDec17[ChapterFilter]
ChapterData.mean(numeric_only='True')
#print(ChapterData.sum(numeric_only='True'))


# In[37]:


# RETRIVE PRACTISE DATA based on PRACTICE CODE, CHAPTER
PracticeCodeFilter = presDec17['PRACTICE'] == 'C83079'
Practice1 = presDec17[PracticeCodeFilter & ChapterFilter]
Practice1Sum = Practice1.sum(numeric_only='True')
print(Practice1Sum)


# In[38]:


# RETRIVE PRACTISE DATA based on PRACTICE CODE, CHAPTER
PracticeCodeFilter2 = presDec17['PRACTICE'] == 'C83633'
Practice2 = presDec17[PracticeCodeFilter2 & ChapterFilter]
Practice2Sum = Practice2.sum(numeric_only='True')
print(Practice2Sum)


# In[39]:


#AVERAGE COST PER UNIT ITEM : "ACT COST" / "ITEMS"
Practice1PerUnit = Practice1Sum[2] / Practice1Sum[0]
Practice2PerUnit = Practice2Sum[2] / Practice2Sum[0]

print("Average cost per unit for Practice 1: "  + str(Practice1PerUnit))
print("Average cost per unit for Practice 2: "  + str(Practice2PerUnit))
print("Difference is: "  + str(Practice1PerUnit - Practice2PerUnit))


# In[45]:


Q59 = presDec17[' SHA'] == 'Q59'
presQ59 = presDec17[Q59]
presQ59.head()


# In[46]:


PracticeData1 = presDec17[PracticeCodeFilter]
PracticeData1.head()


# In[53]:


PracticeDataByChapter = PracticeData1.groupby('CHAPTER')
PracticeDataByChapter.sum()


# In[55]:


PracticeData2 = presDec17[PracticeCodeFilter2]
PracticeData2ByChapter = PracticeData2.groupby('CHAPTER')
PracticeData2ByChapter.sum()


# In[76]:


# GROUP PRACTICE PRESCRIPTION DATA by BNF name
# PracticeDataByBnfName = PracticeData1.groupby('BNF NAME                                    ')
# PracticeDataByBnfName.sum()


# In[75]:


# GROUP PRACTICE PRESCRIPTION DATA by BNF name
# PracticeDataByBnfName2 = PracticeData2.groupby('BNF NAME                                    ')
# PracticeDataByBnfName2.sum()


# In[78]:


# GROUP COMPLETE PRESCRIPTION DATA by Practice code and Chapter
PracticeByChapter = presDec17.groupby(['PRACTICE', 'CHAPTER'])
PracticeByChapter.head(15)


# In[85]:


Practice1

