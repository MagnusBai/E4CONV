#
# http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
import numpy as np
from sklearn.svm import SVC
import pickle

training_data = pickle.load(open('temp/train.pkl', 'r'))
X = np.array(training_data[2])      # E2 (head - tail)
# print X.shape
y = np.array(training_data[0])
print y.shape

clf = SVC()
clf.fit(X, y)
pickle.dump(clf, open('temp/SVM_E2_Model.pkl', 'w'))

