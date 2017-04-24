#
# http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
import numpy as np
from sklearn.svm import SVC
import pickle

test_data = pickle.load(open('temp/test.pkl', 'r'))
X = np.array(test_data[2])      # E2 (head - tail)
# print X.shape
t = np.array(test_data[0])

model = pickle.load()

print t.shape