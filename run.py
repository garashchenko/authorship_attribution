from sklearn.datasets import fetch_mldata
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

mnist = fetch_mldata('MNIST original')

# rescale the data, use the traditional train/test split
X, y = mnist.data / 255., mnist.target
X_train, X_test = X[:60000], X[60000:]
y_train, y_test = y[:60000], y[60000:]

clf = MLPClassifier(hidden_layer_sizes=(600, 300), max_iter=400, alpha=1e-4, solver='sgd', verbose=10, tol=1e-6,
                    random_state=1, learning_rate_init=.1)

clf.fit(X_train, y_train)
print("Training set score: %f" % clf.score(X_train, y_train))
print("Test set score: %f" % clf.score(X_test, y_test))

# Make a prediction
print("Making predictions...")
y_pred = clf.predict(X_test)
acc_rf = accuracy_score(y_test, y_pred)
print(acc_rf)