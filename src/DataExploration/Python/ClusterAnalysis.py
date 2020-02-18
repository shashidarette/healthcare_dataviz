
# coding: utf-8

# ## This notebook is used to extend the data exploration to find clusters within the merged data.
# ## Primarily : AverageAgeProfile of GP, Per patient cost, Value of IMD will be put together.

# In[65]:


from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
#import utils
import pandas as pd
import numpy as np
from itertools import cycle, islice
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

get_ipython().magic('matplotlib inline')


# In[66]:


mergedData = pd.read_csv('./UKMergedDataSelected_u2.csv', sep=',', encoding = "ISO-8859-1")


# In[67]:


mergedData.columns


# In[227]:


features = ['AvgAgeProfile', '% aged 65+ years', '% of Diabetes patients', 'Deprivation score (IMD 2015)', ]


# In[228]:


DiabFilter = mergedData['% of Diabetes patients'] < 15.0
AgeFilter = mergedData['AvgAgeProfile'] < 65.0


# In[233]:


sampleData = mergedData[DiabFilter & AgeFilter]


# In[230]:


sampleData = sampleData[features]


# In[231]:


X = StandardScaler().fit_transform(sampleData)

kmeans = KMeans(n_clusters=4, init='k-means++', n_init=20, max_iter=500,)
model = kmeans.fit(X)
print("model\n", model)

centers = model.cluster_centers_

# Plot clusters - Average age + vs % of Diabetes patients
plt.figure(figsize=(14,7))
colormap = np.array(['b', 'g', 'r', 'm', 'c', 'y', 'k', 'fuchsia', 'peachpuff', 'k', 'm'])
plt.scatter(sampleData['AvgAgeProfile'], sampleData['% of Diabetes patients'], c=colormap[model.labels_], s=40)
plt.title('Clusters - Average age vs % of Diabetes patients')
plt.xlabel("Average GP age")
plt.ylabel(" % of Diabetes patients")


# In[232]:


model.labels_


# In[234]:


sampleData['ClusterNumber'] = model.labels_


# In[235]:


# ClusterDiabetics
sampleData.to_csv('ClusterDiabetics.csv', sep=',')


# In[236]:


features = ['AvgAgeProfile', '% aged 65+ years', '% of Hypertension patients', 'Deprivation score (IMD 2015)', ]


# In[237]:


mergedData['% of Hypertension patients'].describe()


# In[246]:


sampleData = mergedData[mergedData['% of Hypertension patients'] < 25.0]


# In[239]:


sampleData = sampleData[features]


# In[240]:


sampleData.columns


# In[241]:


sampleData.shape


# In[242]:


X = StandardScaler().fit_transform(sampleData)
X


# In[243]:


kmeans = KMeans(n_clusters=3, init='k-means++')
model = kmeans.fit(X)
print("model\n", model)


# In[244]:


centers = model.cluster_centers_
centers


# In[245]:


# Plot clusters - % 65years + vs diabetes
plt.figure(figsize=(14,7))
colormap = np.array(['b', 'g', 'r', 'm', 'c', 'y', 'k', 'w', 'y', 'k', 'w'])
plt.scatter(sampleData['AvgAgeProfile'], sampleData['% of Hypertension patients'], c=colormap[model.labels_], s=40)
plt.title('Clusters - Average age vs % of Hypertension patients')
plt.xlabel("Average GP age")
plt.ylabel(" % of Hypertension patients")


# In[247]:


sampleData['ClusterNumber'] = model.labels_


# In[248]:


# Cluster Hypertension
sampleData.to_csv('ClusterHypertension.csv', sep=',')


# In[104]:


# Plot clusters - % 65years + vs diabetes
plt.figure(figsize=(14,7))
colormap = np.array(['b', 'g', 'r', 'm', 'c', 'y', 'k', 'w'])
plt.scatter(sampleData['AvgAgeProfile'], sampleData['% of Hypertension patients'],  c=colormap[model.labels_], s=40)
plt.title('Clusters - Average age vs % of Hypertension patients')
plt.xlabel("Average GP age")
plt.ylabel(" % of Hypertension patients")


# In[83]:


model


# In[84]:


# Plot clusters - % aged 65+ years vs diabetes
plt.figure(figsize=(14,7))
colormap = np.array(['b', 'g', 'r', 'm', 'c', 'y', 'k', 'w'])
plt.scatter(sampleData['% aged 65+ years'], sampleData['% of Diabetes patients'], c=colormap[model.labels_], s=40)
plt.title('Clusters - %65+ vs  diabetes patient count')
plt.xlabel("% aged 65+ years")
plt.ylabel("Diabetes: QOF prevalence (17+)")


# In[62]:


# Plot clusters - avg. age vs diabetes
plt.figure(figsize=(14,7))
colormap = np.array(['b', 'g', 'r', 'm', 'c', 'y', 'k', 'w'])
plt.scatter(sampleData['% of Diabetes '], sampleData['Deprivation score (IMD 2015)'], c=colormap[model.labels_], s=40)
plt.ylabel("IMD")
plt.xlabel("Diabetes: QOF prevalence (17+)")
plt.title('Clusters - Diabetes patient count vs IMD')


# In[172]:


# Plot clusters - avg. age vs IMD
plt.figure(figsize=(14,7))
colormap = np.array(['b', 'g', 'r', 'm', 'c', 'y', 'k', 'w'])
plt.scatter(sampleData['Deprivation score (IMD 2015)'], sampleData['AvgAgeProfile'], c=colormap[model.labels_], s=40)
plt.title('Clusters - avg. age vs IMD')
plt.xlabel("IMD")
plt.ylabel("AvgAgeProfile")


# In[173]:


# Plot clusters - avg. age vs IMD
plt.figure(figsize=(14,7))
colormap = np.array(['b', 'g', 'r', 'm', 'c', 'y', 'k', 'w'])
plt.scatter(sampleData['Deprivation score (IMD 2015)'], sampleData['% aged 65+ years'], c=colormap[model.labels_], s=40)
plt.title('Clusters - avg. age vs IMD')
plt.xlabel("IMD")
plt.ylabel("% aged 65+")


# In[63]:


# Plot clusters - avg. age vs %65+
plt.figure(figsize=(14,7))
colormap = np.array(['b', 'g', 'r', 'm', 'c', 'y', 'k', 'w'])
plt.scatter(sampleData['AvgAgeProfile'], sampleData['% aged 65+ years'], c=colormap[model.labels_], s=40)
plt.title('Clusters - avg. age vs %65+')


# In[156]:


# Function that creates a DataFrame with a column for Cluster Number

def pd_centers(featuresUsed, centers):
	colNames = list(featuresUsed)
	colNames.append('prediction')

	# Zip with a column called 'prediction' (index)
	Z = [np.append(A, index) for index, A in enumerate(centers)]

	# Convert to pandas data frame for plotting
	P = pd.DataFrame(Z, columns=colNames)
	P['prediction'] = P['prediction'].astype(int)
	return P


# In[157]:


# Function that creates Parallel Plots

def parallel_plot(data):
	my_colors = list(islice(cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']), None, len(data)))
	plt.figure(figsize=(15,8)).gca().axes.set_ylim([-3,+3])
	parallel_coordinates(data, 'prediction', color = my_colors, marker='o')


# In[158]:


P = pd_centers(features, centers)
P


# In[159]:


parallel_plot(P[P['AvgAgeProfile'] != 0])


# # Principal component analysis

# In[160]:


# referred resource : https://www.codementor.io/jadianes/data-science-python-pandas-r-dimensionality-reduction-du1081aka
from sklearn.decomposition import PCA
    
pca = PCA(n_components=2)
pca.fit(sampleData)


# In[161]:


PCA(copy=True, n_components=2, whiten=False)


# In[162]:


existing_2d = pca.transform(sampleData)


# In[163]:


existing_df_2d = pd.DataFrame(existing_2d)
existing_df_2d.index = sampleData.index
existing_df_2d.columns = ['PC1','PC2']
existing_df_2d.head()


# In[164]:


x = existing_df_2d['PC2'] #np.arange(0, UKMergedData['PerPatient_ActCost'].count(), 1.0)
y = existing_df_2d['PC1']
plt.scatter(x, y)
plt.xlabel("PC2")
plt.ylabel("PC1")
plt.show()

