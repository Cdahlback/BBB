import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt

# Pull data
data = pd.read_csv("../data/mn_bbb_businesses_foundVia.csv", low_memory=False).dropna(subset=["BBBRatingScore", "NumberOfEmployees", "NumberOfPartTimeEmployees"])

# Pick independent variables
independent_variables = ["IsBBBAccredited", "BBBRatingScore", "NumberOfEmployees", "NumberOfPartTimeEmployees", "IsHQ", "IsCharity"]

# Pull all rows from independent variables
X = data.loc[:, independent_variables]

# Pull all rows from dependent variable (FoundVia)
Y = data.iloc[:, -1]

# Build decision tree (Classification)
clf = tree.DecisionTreeClassifier(max_depth=6)
clf = clf.fit(X, Y)

# Plot the tree for visualization
found_via = ['BBB', 'Email', 'Search']
plt.figure(figsize=(80, 80))
tree.plot_tree(clf, class_names=found_via, feature_names=independent_variables, filled=True, fontsize=8)
# plt.show()
plt.savefig('tree', dpi=200)
