import os
import sys
import img_utils
import cv2
import yaml
import pickle
import numpy as np

def find_phone(clf, params, img):
    # Use the classifier model to predict probabilites over the different windows 
    # generated over test image and pick center of the one with maximum probability
    (centers,windows) = img_utils.create_windows(params,img)
    probs = clf.predict_proba( windows )[:,1]
    return centers[np.argmax( probs )]



if __name__=='__main__':
    if (len(sys.argv) < 2):
        print("Insufficient number of arguments provided.\
            Provide Path to the image. (e.g ./find_phone_test_iamges/0.jpg)")
    if not os.access(sys.argv[1], os.W_OK):
        print("Path Invalid")

    img_path = sys.argv[1]
    config_path = os.path.join(os.path.abspath(os.path.curdir),"config.yaml")

    with open(config_path) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        params = yaml.load(file, Loader=yaml.FullLoader)
    params['testing_fraction'] = 1.0 - params['training_fraction']

    model_path = os.path.join(os.path.abspath(os.path.curdir),"clf_model.pickle")
    with open(model_path, 'rb') as model_file:
        clf = pickle.load(model_file)

    data_path = os.path.join(os.path.abspath(os.path.curdir),"data.pickle")
    with open(data_path, 'rb') as data_file:
        data = pickle.load(data_file)

    img = cv2.imread(img_path)
    img = img_utils.preprocess_img(img)
    center = find_phone(clf, params, img)
    print("{0:.4f}   {1:.4f}".format(center[0],center[1]))