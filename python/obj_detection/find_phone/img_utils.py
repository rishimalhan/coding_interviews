import random
import cv2
import numpy as np
import time

def preprocess_images(data):
    for key in data['img_list'].keys():
        data['img_list'][key] = cv2.cvtColor(data['img_list'][key], cv2.COLOR_BGR2GRAY)

def prep_train_image(img,center,side,hght,width):
    crop_box = map(int, [(center[0]-side)*img.shape[1], (center[1]-side)*img.shape[0],
                            (center[0]+side)*img.shape[1], (center[1]+side)*img.shape[0] ] )
    crop_box = [0 if i < 0 else i for i in crop_box]
    # Image with phone
    img = cv2.resize( img[crop_box[1]:crop_box[3],crop_box[0]:crop_box[2]],
                        (hght, width) )
    return img

def prep_XY_set(data,params,ids):
    ip = []
    op = []
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
            center = [random.uniform(0+side,1-side),random.uniform(0+side,1-side)]
            img = prep_train_image(img,center,side,hght,width)
            ip.append( np.array(img).flatten() )
            op.append( 0 )
    return (np.array(ip),np.array(op))