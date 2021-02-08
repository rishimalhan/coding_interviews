import numpy as np
import cv2
import pandas as pd
import data_handler
import yaml
import sys
import os
import img_utils
import classifiers
import pickle
import model_analysis

def main(path,params):
    # Inputs: 
    # path: type: str, func: path to the data 
    # params: type: dictionary, func: parameter values to be used in algorithm
    
    print("Reading the data from files and parsing it into custom data structures")
    data = data_handler.read_data(path,params)
    print("Preprocessing all Images")
    img_utils.preprocess_images(data)
    
    print("Training the classifier to distinguish between images with and without phone")
    (training_set,testing_set) = data_handler.prepare_datasets( data,params )
    clf = classifiers.logistic_regression(training_set[0],training_set[1])
    print("Checking model accuracies")
    model_analysis.model_accuracy(clf,testing_set[0],testing_set[1])
    model_analysis.alg_accuracy(clf,params,data)

if __name__=='__main__':
    # Validate inputs
    if (len(sys.argv) < 2):
        print("Insufficient number of arguments provided.\
            Provide Path to the dataset directory. (e.g ./find_phone)")
    if not os.access(sys.argv[1], os.W_OK):
        print("Path Invalid")

    path = sys.argv[1]

    # load parameter values
    config_path = os.path.join(os.path.abspath(os.path.curdir),"config.yaml")
    with open(config_path) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        params = yaml.load(file, Loader=yaml.FullLoader)
    params['testing_fraction'] = 1.0 - params['training_fraction']

    main(path,params)