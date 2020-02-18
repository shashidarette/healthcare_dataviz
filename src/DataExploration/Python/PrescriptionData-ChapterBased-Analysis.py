
# coding: utf-8

# ### Analysis of Prescription costs based on below categories
# * 0601021* Oral hypoglycaemics
# * 0601022* Metformin
# * 0601023* Gliptins
# * 0601011* Insulin
# * 0601012*Insulin
# * 0704050* Viagra and others

# In[1]:


import pandas as pd
presDec17 = pd.read_csv('./T201712PDPI+BNFT.CSV', sep=',', encoding = "ISO-8859-1")
print(type(presDec17))
presDec17.head(15)


# In[2]:


presDec17.describe()


# In[3]:


# UPDATE CHAPTER NUMBER - BASED ON MEDICINES OF INTRESET
presDec17['CHAPTER'] = presDec17['BNF CODE'].str[:2]
presDec17.head()


# In[4]:


# UPDATE SUB-CHAPTER NUMBER - 2 characters of BNF CODE
presDec17['SUB_CHAPTER'] = presDec17['BNF CODE'].str[:7]
presDec17.head()


# In[5]:


# UPDATE SUB-CHAPTER NUMBER - 2 characters of BNF CODE
presDec17['SUB_CHAPTER_REM'] = presDec17['BNF CODE'].str[7:]
presDec17.head()


# In[6]:


# GROUP the prescription data by Practice code and Sub_Chapter
PracticeBySubChapter = presDec17.groupby(['PRACTICE', 'SUB_CHAPTER'])
PracticeBySubChapter.head(15)


# In[7]:


PracticeBySubChapterSum = PracticeBySubChapter.sum()


# In[8]:


# PracticeBySubChapterSum output
PracticeBySubChapterSum.to_csv('PracticeBySubChapterSum.csv', sep=',')


# In[10]:


presDec17.columns


# In[7]:


PracticeBySubChapByCode = presDec17.groupby(['PRACTICE', 'SUB_CHAPTER', 'SUB_CHAPTER_REM'])


# In[9]:


PracticeBySubChapByCode.sum().to_csv('PracticeBySubChapterByBNF.csv', sep=',')


# In[10]:


PracticeBySubChapByCode.describe()


# In[ ]:


PracticeBySubChapByCode.head()


# In[24]:


BNFCodeNameMap = presDec17[['BNF CODE', 'BNF NAME                                    ', 'SUB_CHAPTER', 'SUB_CHAPTER_REM', 'ITEMS  ',
       'NIC        ', 'ACT COST   ', 'QUANTITY']]


# In[25]:


BNFCodeNameMapUnique = BNFCodeNameMap.drop_duplicates(['BNF CODE'])


# In[26]:


BNFCodeNameMap.head


# In[27]:


BNFCodeNameMapUnique.head


# In[29]:


BNFCodeNameMapUnique.to_csv('BNF_CodeNameCostMap.csv', sep=',')


# In[23]:


BNFCodeNameMap.to_csv('BNF_CodeNameCostMapDupli.csv', sep=',')

