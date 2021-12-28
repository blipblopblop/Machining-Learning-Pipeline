#!/usr/bin/env python
# coding: utf-8

# # **Space X  Falcon 9 First Stage Landing Prediction**
# 

# ## Machine Learning Prediction
# 

# Space X advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because Space X can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against space X for a rocket launch.   In this lab, you will create a machine learning pipeline  to predict if the first stage will land given the data from the preceding labs.
# 

# ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/landing\_1.gif)
# 

# Several examples of an unsuccessful landing are shown here:
# 

# ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/crash.gif)
# 

# Most unsuccessful landings are planed. Space X; performs a controlled landing in the oceans.
# 

# ## Objectives
# 

# Perform exploratory  Data Analysis and determine Training Labels
# 
# *   create a column for the class
# *   Standardize the data
# *   Split into training data and test data
# 
# \-Find best Hyperparameter for SVM, Classification Trees and Logistic Regression
# 
# *   Find the method performs best using test data
# 

# ***
# 

# ## Import Libraries and Define Auxiliary Functions
# 

# Importing the following libraries for the lab
# 

# In[2]:


# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
# Preprocessing allows us to standarsize our data
from sklearn import preprocessing
# Allows us to split our data into training and testing data
from sklearn.model_selection import train_test_split
# Allows us to test parameters of classification algorithms and find the best one
from sklearn.model_selection import GridSearchCV
# Logistic Regression classification algorithm
from sklearn.linear_model import LogisticRegression
# Support Vector Machine classification algorithm
from sklearn.svm import SVC
# Decision Tree classification algorithm
from sklearn.tree import DecisionTreeClassifier
# K Nearest Neighbors classification algorithm
from sklearn.neighbors import KNeighborsClassifier


# This function is to plot the confusion matrix.
# 

# In[3]:


def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed'])


# ## Load the dataframe
# 

# Load the data
# 

# In[4]:


data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# If you were unable to complete the previous lab correctly you can uncomment and load this csv

# data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_2.csv')

data.head()


# In[5]:


X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv')

# If you were unable to complete the previous lab correctly you can uncomment and load this csv

# X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_3.csv')

X.head(100)


# ## Sorting the data 
# 

# Create a NumPy array from the column <code>Class</code> in <code>data</code>, by applying the method <code>to_numpy()</code>  then
# assign it  to the variable <code>Y</code>,make sure the output is a  Pandas series (only one bracket df\['name of  column']).
# 

# In[7]:


Y = data['Class'].to_numpy()
print(Y)


# ## Cleaning the data
# 

# Standardize the data in <code>X</code> then reassign it to the variable  <code>X</code> using the transform provided below.
# 

# In[8]:


# students get this 
transform = preprocessing.StandardScaler()


# In[9]:


x_scaled = transform.fit_transform(X)
X = pd.DataFrame(x_scaled)
print(X)


# We split the data into training and testing data using the  function  <code>train_test_split</code>.   The training data is divided into validation data, a second set used for training  data; then the models are trained and hyperparameters are selected using the function <code>GridSearchCV</code>.
# 

# ## Forming the training and test data
# 

# Use the function train_test_split to split the data X and Y into training and test data. Set the parameter test_size to  0.2 and random_state to 2. The training data and test data should be assigned to the following labels.
# 

# <code>X_train, X_test, Y_train, Y_test</code>
# 

# In[10]:


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
print(X_train, X_test, Y_train, Y_test)


# we can see we only have 18 test samples.
# 

# In[11]:


Y_test.shape


# ## HyperParameter Tuning with GridSearchCV 

# GridSearchCV is the process of performing hyperparamter tuning in order to determine the optimal values for a given model. To do so, predefined values for hyperparameters are passed to the GridSearchCV function through a dictionary. The function uses cross-validation method to try all combinations of the given hyperparameters. Afterwhich, the function is used to obtain the accuracy/loss of each combination wherein user can choose the one with the best performance.
# 
# source: https://www.mygreatlearning.com/blog/gridsearchcv/

# ## Logistic-Regression
# 

# Create a logistic regression object  then create a  GridSearchCV object  <code>logreg_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.
# 
# Logistic Regression is a classification technique that falls under a linear classifier. It determines the best preditced weigths (aka coefficents/parameters) through the maximum likelihood estimation which maximizes the log-likilood functions for obervations i = 1, ..., i, represented the by equations LLF = Σᵢ(𝑦ᵢ log(𝑝(𝐱ᵢ)) + (1 − 𝑦ᵢ) log(1 − 𝑝(𝐱ᵢ))). 
# 
# source: https://realpython.com/logistic-regression-python/#classification

# In[12]:


parameters ={'C':[0.01,0.1,1],
             'penalty':['l2'],
             'solver':['lbfgs']}


# In[13]:


parameters ={"C":[0.01,0.1,1],'penalty':['l2'], 'solver':['lbfgs']}# l1 lasso l2 ridge
lr=LogisticRegression()
logreg_cv = GridSearchCV(lr,parameters,cv=5)
logreg_cv.fit(X_train, Y_train)
print(logreg_cv.best_params_)


# We output the <code>GridSearchCV</code> object for logistic regression. We display the best parameters using the data attribute <code>best_params\_</code> and the accuracy on the validation data using the data attribute <code>best_score\_</code>.
# 

# In[14]:


print("tuned hpyerparameters :(best parameters) ",logreg_cv.best_params_)
print("accuracy :",logreg_cv.best_score_)


# ## Accuracy of Logistic Regression 
# 

# Calculate the accuracy on the test data using the method <code>score</code>:
# 

# In[15]:


logreg_cv.score(X,Y)


# Lets look at the confusion matrix:
# 

# In[17]:


yhat=logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)


# Examining the confusion matrix, we see that logistic regression can distinguish between the different classes.  We see that the major problem is false positives.
# 

# ## Support Vector Machine Classification
# 

# Create a support vector machine object then  create a  <code>GridSearchCV</code> object  <code>svm_cv</code> with cv - 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>. 
# 
# The support vector machine classification is an alogorithm used to find a hyperplane in the N-dimensional space that has maximum margin - maximum distanace between the data points of the classes.
# 
# sources:https://towardsdatascience.com/support-vector-machine-introduction-to-machine-learning-algorithms-934a444fca47 , https://web.mit.edu/6.034/wwwbob/svm.pdf
# 

# In[21]:


parameters = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma':np.logspace(-3, 3, 5)}
svm = SVC()


# In[63]:


svm.fit(X_train, Y_train)
svm_cv = GridSearchCV(svm,parameters,n_jobs=-10)
svm_cv.fit(X_train, Y_train)


# In[64]:


print("tuned hpyerparameters :(best parameters) ",svm_cv.best_params_)
print("accuracy :",svm_cv.best_score_)


# Calculate the accuracy on the test data using the method <code>score</code>:
# 

# In[65]:


svm_cv.score(X,Y)


# We can plot the confusion matrix
# 

# In[67]:


yhat=svm_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)


# ## Decision Tree Classifier
# 

# Create a decision tree classifier object then  create a  <code>GridSearchCV</code> object  <code>tree_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.
# 
# The decision tree classifier is a machine learning classification algorithm that can perform classification and regression tasks wherein the intuition is to use yes/no questions to continually split the data until it is all sorted. A node in a decision tree represents an instance, answers to the questions earlier asked (yes/no) are represented by the branch, and the leaf node is the class label.
# 
# sources: https://towardsdatascience.com/decision-tree-classifier-explained-in-real-life-picking-a-vacation-destination-6226b2b60575 , https://www.sciencedirect.com/topics/computer-science/decision-tree-classifier

# In[82]:


parameters = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}

tree = DecisionTreeClassifier()


# In[85]:


#no .fit() tree
tree_cv = GridSearchCV(tree,parameters,n_jobs=10)
tree_cv.fit(X_train, Y_train)


# In[84]:


print("tuned hpyerparameters :(best parameters) ",tree_cv.best_params_)
print("accuracy :",tree_cv.best_score_)


# Calculate the accuracy of tree_cv on the test data using the method <code>score</code>:
# 

# In[86]:


tree_cv.score(X,Y)


# We can plot the confusion matrix
# 

# In[88]:


yhat = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)


# ## K-Nearest Neighbors Algorithm
# 

# Create a k nearest neighbors object then  create a  <code>GridSearchCV</code> object  <code>knn_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.
# 
# The K nearest neighbours (KNN) algorithm can be used to solving classification and regression problems wherin it classfies the data based on the classfication labels of nearby data. 
# 
# sources: https://towardsdatascience.com/machine-learning-basics-with-the-k-nearest-neighbors-algorithm-6a6e71d01761
# 

# In[89]:


parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1,2]}

KNN = KNeighborsClassifier()


# In[92]:


KNN.fit(X_train, Y_train)
KNN_cv = GridSearchCV(KNN,parameters,n_jobs=10)
KNN_cv.fit(X_train, Y_train)


# In[95]:


print("tuned hpyerparameters :(best parameters) ",KNN_cv.best_params_)
print("accuracy :",KNN_cv.best_score_)


# Calculate the accuracy of tree_cv on the test data using the method <code>score</code>:
# 

# In[96]:


KNN_cv.score(X,Y)


# We can plot the confusion matrix
# 

# In[98]:


yhat = KNN_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)


# ## Authors
# 

# <a href="https://www.linkedin.com/in/joseph-s-50398b136/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2021-01-01">Joseph Santarcangelo</a> has a PhD in Electrical Engineering, his research focused on using machine learning, signal processing, and computer vision to determine how videos impact human cognition. Joseph has been working for IBM since he completed his PhD.
# 

# ## Change Log
# 

# | Date (YYYY-MM-DD) | Version | Changed By    | Change Description      |
# | ----------------- | ------- | ------------- | ----------------------- |
# | 2021-08-31        | 1.1     | Lakshmi Holla | Modified markdown       |
# | 2020-09-20        | 1.0     | Joseph        | Modified Multiple Areas |
# 

# Copyright © 2020 IBM Corporation. All rights reserved.
# 
