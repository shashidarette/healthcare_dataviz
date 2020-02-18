
# coding: utf-8

# ## This notebook is used to merge the costs at drug groups selected with main cluster diabetes data

# In[ ]:


import pandas as pd


# In[2]:


# Update the clusters from ClusterDiabetics.csv generated using ClusterAnalysis jupyter notebook
ClusterDiabetes = pd.read_csv('./DataMergingFiles/ClusterDiabetics.csv', sep=',', encoding = "ISO-8859-1")


# In[4]:


CostsGliptins = pd.read_csv('./DataMergingFiles/CostsByGliptinsByCluster.csv', sep=',', encoding = "ISO-8859-1")
CostsInsulin = pd.read_csv('./DataMergingFiles/CostsByInsulinByCluster.csv', sep=',', encoding = "ISO-8859-1")
CostsMetformin = pd.read_csv('./DataMergingFiles/CostsByMetforminByCluster.csv', sep=',', encoding = "ISO-8859-1")
CostsOral = pd.read_csv('./DataMergingFiles/CostsByOralByCluster.csv', sep=',', encoding = "ISO-8859-1")
CostsViagra = pd.read_csv('./DataMergingFiles/CostsByViagraByCluster.csv', sep=',', encoding = "ISO-8859-1")


# In[6]:


CostsInsulin['SUB_CHAPTER'].unique()


# In[9]:


CostsInsulin1_Filter = CostsInsulin['SUB_CHAPTER'] == 601011
CostsInsulin2_Filter = CostsInsulin['SUB_CHAPTER'] == 601012


# In[10]:


CostsInsulin1 = CostsInsulin[CostsInsulin1_Filter]
CostsInsulin2 = CostsInsulin[CostsInsulin1_Filter]


# In[13]:


CostsDataMerged = ClusterDiabetes.merge(CostsMetformin, left_on='PRACTICE', right_on='PRACTICE', how='inner')
CostsDataMerged = CostsDataMerged.merge(CostsGliptins, left_on='PRACTICE', right_on='PRACTICE', how='inner')
CostsDataMerged = CostsDataMerged.merge(CostsOral, left_on='PRACTICE', right_on='PRACTICE', how='inner')
CostsDataMerged = CostsDataMerged.merge(CostsViagra, left_on='PRACTICE', right_on='PRACTICE', how='inner')
CostsDataMerged = CostsDataMerged.merge(CostsInsulin1, left_on='PRACTICE', right_on='PRACTICE', how='inner')
CostsDataMerged = CostsDataMerged.merge(CostsInsulin2, left_on='PRACTICE', right_on='PRACTICE', how='inner')
CostsDataMerged.describe()
CostsDataMerged.head


# In[14]:


CostsDataMerged.to_csv("CostsDataMerged.csv", sep=',')

