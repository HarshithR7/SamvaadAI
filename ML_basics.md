Scikit-Learn, Tensorflow and Keras are the entry points to machine learning.

## Machine Learning
> Machine Learning is a field of study that gives computers the ability to learn on its own without being programmed explicitly.

> Data Mining is applying ML techniques to dig into large amounts of data to discover patterns that were not immediately apparent.

Regression tasks (Prediction values).
> RNN, CNN, RL, Transformers. 

## Types of Machine Learning Systems

### Based on Training - 
**Supervised** -  In supervised learning, the training set you feed to the algorithm includes the desired solutions, called labels.
• k-Nearest Neighbors
• Linear Regression
• Logistic Regression
• Support Vector Machines (SVMs)
• Decision Trees and Random Forests
• Neural networks

**Unsupervised**- the training data is unlabeled.
• Clustering
— K-Means
— DBSCAN
— Hierarchical Cluster Analysis (HCA) -  it subdivides each group into smaller groups
• Anomaly detection and novelty detection - detecting unusual credit card transactions to prevent fraud, catching manufacturing defects,
or automatically removing outliers from a dataset before feeding it to another learning algorithm.
— One-class SVM
— Isolation Forest
• Visualization and dimensionality reduction
— Principal Component Analysis (PCA)
— Kernel PCA
— Locally Linear Embedding (LLE)
— t-Distributed Stochastic Neighbor Embedding (t-SNE)
• Association rule learning - dig into large amounts of data and discover interesting relations between attributes.
— Apriori
— Eclat

**Semisupervised learning**- Google Photos, are good examples 
**Reinforcement Learning** - Reinforcement Learning is learning by trial and error, where an agent learns what to do—how to map situations to actions—to maximize cumulative reward.
### Based on Learning
**Batch Learning (Offline Learning)** - The model is trained on the entire dataset at once (or in large chunks called batches). Training is done offline, and the model doesn’t learn after deployment unless retrained - when data is fixed- it learns on global data at once.
**Online Learning (Incremental Learning)** - The model learns incrementally, processing one data point or mini-batch at a time. It can adapt continuously as new data comes in.

<details>
import sklearn.linear_model
model = sklearn.linear_model.LinearRegression()
with these two:
import sklearn.neighbors
model = sklearn.neighbors.KNeighborsRegressor(n_neighbors=3)
</details>

### Main Challenges of ML - Bad data (Quality or quantity) & Bad Algorithm


**Overfitting**	Model learns the training data too well, including noise and details that don't generalize.
**Underfitting**	Model is too simple, fails to capture the underlying patterns in the data.
**Feature Selection, Feature Extraction**
**Training, Evaluate and Fine-Tune**

> A sequence of data processing components is called a data pipeline.
> Answer - supervise, unsupervised or RL. classification or regression. online learning or batch learning.
