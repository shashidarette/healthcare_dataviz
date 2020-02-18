
# coding: utf-8

# # This notebook is used to combine the sub-chapter level prescription data and diabetes clustered data based on practice code

# In[1]:


import pandas as pd


# In[2]:


# Update the clusters from ClusterDiabetics.csv generated using ClusterAnalysis jupyter notebook
ClusterDiabetes = pd.read_csv('./ClusterDiabetics.csv', sep=',', encoding = "ISO-8859-1")


# In[3]:


# Load PracticeBySubChapterSum.csv into a new DataFrame - PracticeBySubChapterSum.csv
PracticeBySubChapterSum = pd.read_csv('./PracticeBySubChapterSum.csv', sep=',', encoding = "ISO-8859-1")


# In[5]:


ClusterFeatures = ['PRACTICE', 'ClusterNumber']


# In[6]:


PracticeByCluster = ClusterDiabetes[ClusterFeatures]


# In[8]:


PracticeBySubChapterSum.columns


# In[10]:


PracticeBySubChapterSumMerged = PracticeBySubChapterSum.merge(PracticeByCluster, left_on='PRACTICE', right_on='PRACTICE', how='inner')
PracticeBySubChapterSumMerged.head()


# In[12]:


PracticeBySubChapterSumMerged.drop(columns=['PERIOD'])


# In[13]:


# Save combined data into PracticeBySubChapterClustered.csv
PracticeBySubChapterSumMerged.to_csv("PracticeBySubChapterClustered.csv", sep=',')


# In[23]:


# Filter the combined data by cluster and save it & Save data into PracticeBySubChapterByCluster.csv
UniqueClusters = PracticeBySubChapterSumMerged['ClusterNumber'].unique()
for cluster in UniqueClusters:
    ClusterFilter = PracticeBySubChapterSumMerged['ClusterNumber'] == cluster
    PracticeBySubChapterByClusterData = PracticeBySubChapterSumMerged[ClusterFilter]
    ClusterFileName = "PracticeBySubChapterByCluster_" + str(cluster) + ".csv"
    PracticeBySubChapterByClusterData.to_csv(ClusterFileName, sep=',')

