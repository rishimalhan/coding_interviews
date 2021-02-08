from sklearn.linear_model import LogisticRegression
import os
import pickle
from sklearn.metrics import accuracy_score

# DIfferent classifiers to be used to classify images which have the phone in them and the ones which donot

def logistic_regression(X,Y):
    train_param_path = os.path.join(os.path.abspath(os.path.curdir),"clf_model.pickle")
    clf = LogisticRegression().fit(X, Y)
    with open(train_param_path, 'wb') as file_out:
        pickle.dump(clf, file_out)
    return clf
