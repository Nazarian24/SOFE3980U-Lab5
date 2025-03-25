import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from cleanlab.classification import CleanLearning

iris = load_iris()
X = iris.data
y = iris.target

np.random.seed(42)
num_errors = 15
error_indices = np.random.choice(len(y), num_errors, replace=False)
y[error_indices] = np.random.choice([0, 1, 2], num_errors, replace=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
cleaner = CleanLearning(clf)
cleaner.fit(X_train, y_train)

label_issues = cleaner.find_label_issues(X=X_train, labels=y_train)
mislabeled_indices = np.where(label_issues["is_label_issue"])[0]
print(f"\nDetected {len(mislabeled_indices)} suspected label errors at indices:\n{mislabeled_indices}")

if len(mislabeled_indices) > 0:
    predicted_labels = cleaner.predict(X_train)
    suspect_data = []
    
    for idx in mislabeled_indices:
        suspect_data.append({
            'Index': idx,
            'Sepal Length': X_train[idx, 0],
            'Sepal Width': X_train[idx, 1],
            'Petal Length': X_train[idx, 2],
            'Petal Width': X_train[idx, 3],
            'Original Label': iris.target_names[y_train[idx]],
            'Suggested Label': iris.target_names[predicted_labels[idx]],
            'Confidence': np.max(cleaner.predict_proba(X_train[idx:idx+1]))
        })
    
    df_suspects = pd.DataFrame(suspect_data)
    
    print("\nSuspected Mislabeled Data Points:")
    print("="*80)
    print(df_suspects.to_string(index=False, float_format="%.1f"))
    
    print("\nFeature Statistics for Verification:")
    print("Class 0 (Setosa) avg petal length:", np.mean(X_train[y_train==0, 2]))
    print("Class 1 (Versicolor) avg petal length:", np.mean(X_train[y_train==1, 2]))
    print("Class 2 (Virginica) avg petal length:", np.mean(X_train[y_train==2, 2]))
else:
    print("\nWARNING: No label issues detected.")

df_suspects.to_csv('detected_label_issues.csv', index=False)
print("\nResults saved to 'detected_label_issues.csv'")
