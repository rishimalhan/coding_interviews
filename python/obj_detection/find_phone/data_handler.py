from glob import glob
import cv2
import numpy as np
import math
import copy
import pandas as pd
import img_utils
import model_analysis

def read_data(folder_path,params):
    # Inputs:
    # folder_path: type: str, func: path to the data
    # params: type: dictionary, func: parameter values to be used in algorithm
    # Output:
    # data: type: dictionary, func: provide all images and corresponding image ids, training and test ids and labels

    image_paths = glob(folder_path + '/*.jpg')
    image_list = {}
    image_ids = np.array([],dtype=int)
    for img in image_paths:
        img_id = int(img.split(folder_path+"/")[1].split(".jpg")[0])
        image_list[img_id] = cv2.imread(img)
        image_ids = np.append( image_ids, img_id )

    image_ids_cpy = copy.deepcopy(image_ids)
    np.random.shuffle( image_ids_cpy )
    no_training_ids = int(math.ceil(params['training_fraction']*\
                                image_ids.shape[0]))
    training_data_indices = image_ids_cpy[0:no_training_ids]
    testing_data_indices = image_ids_cpy[no_training_ids:]

    labels_file = folder_path+"/labels.txt"
    labels_list = np.array( pd.read_csv( labels_file, header=None, sep=' ' ) )
    label_ids = np.array(labels_list[:,0],dtype=str)
    label_x = np.array(labels_list[:,1],dtype=float)
    label_y = np.array(labels_list[:,2],dtype=float)
    labels = {}
    for i,val in enumerate(np.char.split(label_ids, sep=".jpg")[0:]):
        labels[int(val[0])] = [ label_x[i],label_y[i] ]

    data = {}
    data['img_list'] = image_list
    data['img_ids'] = image_ids
    data['train_ids'] = training_data_indices
    data['test_ids'] = testing_data_indices
    data['labels'] = labels

    return data


def prepare_datasets(data,params):
    # Inputs:
    # data: type: dictionary, func: provide all images and corresponding image ids, training and test ids and labels
    # We use the data for generating training and testing data set
    # Outputs:
    # Function returns a tuple of training and testing data sets
    # training and testing data set is in turn a tuple of np array of flattened image and corresponding label
    return (img_utils.prep_XY_set(data,params,data['train_ids']),
                img_utils.prep_XY_set(data,params,data['test_ids']))