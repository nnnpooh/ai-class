#%%
import __main__ as main

try:
    hasattr(main, "__file__")
    from IPython import get_ipython

    get_ipython().magic("reset -sf")
    get_ipython().magic("clear")
except:
    pass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from PlotFunction import plot_decision_surface

plt.close("all")
# =============================================================================
# Program start
# =============================================================================
# Model parameters
eta = 0.1

# Read/format data
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
df = pd.read_csv(url, header=None)

# Extract y values and perform feature extraction
y = df.iloc[0:100, 4].values
# Note that here you can use any value to distinguish betwee two classes.
y = np.where(y == "Iris-setosa", 0, 1)
# y = np.where(y == "Iris-setosa", -1, 1)
# y = np.where(y == "Iris-setosa", 0, 10)

# Extract sepal length and petal length
X = df.iloc[0:100, [0, 2]].values

# Standardization
sc = StandardScaler()
sc.fit(X)
X_std = sc.transform(X)

# Create object (estimator)
lr = LogisticRegression(random_state=2, verbose=1, solver="liblinear")

# Training
lr.fit(X_std, y)

# Extracting coefficients
W = np.append(lr.intercept_.flatten(), lr.coef_.flatten())

# Count misclassification
yHat = lr.predict(X_std)
numFalse = (y != yHat).sum()

print(
    f"\nnumFalse = {numFalse:3d},  " "W =",
    np.array2string(W, formatter={"float_kind": lambda x: "%.4f" % x}),
)

# Append a columne of X0
x0 = np.ones((X.shape[0], 1))
X_std = np.hstack((x0, X_std))

# Plotting decision surface
plot_decision_surface(y, X_std, W, "perceptron", filename="output.png")
