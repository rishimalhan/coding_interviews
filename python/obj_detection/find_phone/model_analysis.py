import find_phone
from sklearn.metrics import accuracy_score
import numpy as np

def alg_accuracy(clf, params, data):
    pred_centers = []
    true_center = []
    for key in data['img_list'].keys():
        center = find_phone.find_phone(clf, params,data['img_list'][key] )
        pred_centers.append(center)
        true_center.append( data['labels'][key] )

    thresh = params['viol_thresh']
    num_viols = np.where(np.linalg.norm( np.array(pred_centers)-
                    np.array(true_center),axis=1 ) > thresh)[0].shape[0]
    print("Using threshold value of {0} for finding accuracy".format(thresh))
    print( "Accuracy of detecting centers over all images: ", 
                1.0-(float(num_viols)/float(len(pred_centers))) )


def model_accuracy(clf,X,true_y):
    y = clf.predict(X)
    accuracy_score(true_y,y)
    print("\n")
    print("Accuracy of classifying with vs without phone images: {0}".format(accuracy_score(true_y,y)))