import random
import cv2
import numpy as np
import imutils

def preprocess_img(img):
    # Apply preprocessing
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def preprocess_images(data):
    for key in data['img_list'].keys():
        data['img_list'][key] = preprocess_img(data['img_list'][key])

def prep_train_image(img,center,side,hght,width):
    # Prepare a cropping square and crop the image
    crop_box = map(int, [(center[0]-side)*img.shape[1], (center[1]-side)*img.shape[0],
                            (center[0]+side)*img.shape[1], (center[1]+side)*img.shape[0] ] )
    crop_box = [0 if i < 0 else i for i in crop_box] # If crop box has negative values then reset it to 0. Pending: apply max value as well
    # Image with phone
    img = cv2.resize( img[crop_box[1]:crop_box[3],crop_box[0]:crop_box[2]],
                        (hght, width) )
    return img

def prep_XY_set(data,params,ids):
    # Inputs:
    # data: type: dictionary, func: provide all images and corresponding image ids, training and test ids and labels
    # We use the data for generating training and testing data set
    # ids correspond to the keys for an image and corresponding label. For e.g 0.jpg has a key of 0
    # Ouput:
    # Returns the tuple of i/p X and o/p Y
    # Algorithm: Take each image and preprocess it (e.g. convert to greyscale)
    # Take the image center from labels and construct a window around it of length specified in params (label: 1)
    # Construct windows from other parts of image (label: 0)
    # Merge the data set and randomize it
    ip = []
    op = []
    random.seed(0)
    side = params['normalized_half_phone_box_length']
    hght = params['dwnsample_hght']
    width = params['dwnsample_width']
    for idx in ids:
        img = data['img_list'][idx]
        center = data['labels'][idx]
        img = prep_train_image(img,center,side,hght,width)
        ip.append( np.array(img).flatten() )
        op.append( 1 )

        for i in range(params['dataset_ratio']):
            # ToDo checkers for making sure image box is not outside
            center = [random.uniform(0+side,1-side),random.uniform(0+side,1-side)] # Make sure crop box doesnt go out of the image
            img = prep_train_image(img,center,side,hght,width)
            ip.append( np.array(img).flatten() )
            op.append( 0 )
    combined = np.column_stack(( np.array(ip),np.array(op) ))
    np.random.shuffle(combined)
    return ( combined[:,0:-1],combined[:,-1] )

def create_windows(params,img):
    # Take a preprocessed image and uniformly sample centers on the image. Then crop windows around these centers which will be used for predictions
    window_list = []
    centers = []
    num_windows = params['numb_windows_sampled']
    side = params['normalized_half_phone_box_length']
    hght = params['dwnsample_hght']
    width = params['dwnsample_width']
    for i in np.linspace(0+side,1-side,num_windows):
        for j in np.linspace(0+side,1-side,num_windows):
            center = [i,j]
            # center = [random.uniform(0+side,1-side),random.uniform(0+side,1-side)]
            centers.append( center )
            window_list.append( np.array(prep_train_image(img,center,side,hght,width)).flatten() )
    return (centers,np.array(window_list))