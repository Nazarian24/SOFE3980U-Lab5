import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from cleanlab.classification import CleanLearning


iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = iris.target


np.random.seed(42)
anomaly_indices = np.random.choice(df.index, size=10, replace=False)
df.loc[anomaly_indices, 'petal length (cm)'] = np.random.uniform(5, 7, size=10)


clf = CleanLearning()
clf.fit(df[iris.feature_names], df['species'])
issues = clf.find_label_issues(df[iris.feature_names], df['species'])
anomalies = np.where(issues["is_label_issue"])[0]


species_names = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}
results = []

for idx in anomalies:
    row = df.iloc[idx]
    results.append({
        'Index': idx,
        'Sepal Length': row['sepal length (cm)'],
        'Sepal Width': row['sepal width (cm)'],
        'Petal Length': row['petal length (cm)'],
        'Petal Width': row['petal width (cm)'],
        'Label': species_names[row['species']],
        'Is Anomaly': True
    })

print("\nDetected Anomalies:")
print(pd.DataFrame(results).to_string(index=False))
