import random
import cv2
import numpy as np
import imutils

def preprocess_img(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def preprocess_images(data):
    for key in data['img_list'].keys():
        data['img_list'][key] = preprocess_img(data['img_list'][key])

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

def create_windows(params,img):
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

    center = contour_bias_center(img)
    if center:
        centers.append(center)
        window_list.append( np.array(prep_train_image(img,center,side,hght,width)).flatten() )    

    return (centers,np.array(window_list))

def contour_bias_center(gray):
    #convert image to binary and invert (for contours)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.bitwise_not(thresh)

    #calculate contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    N = len(cnts)

    #if no proper contours calculated
    if not N:
        return []
    #else, contour "algorithm" to detect phone contour
    else:
        cnts_values = np.ones(N)*np.maximum(gray.shape[0],gray.shape[1])
        for i in range(N):
            param = cv2.arcLength(cnts[i],True)/4
            area = np.sqrt(cv2.contourArea(cnts[i]))
            if (param>10) and (area>10):
                cnts_values[i] = np.absolute(param-area)/np.minimum(param,area)
        phone = np.argmin(cnts_values)

        #calculate and print center
        M = cv2.moments(cnts[phone])
        cX = int(M["m10"] / M["m00"]) / gray.shape[1]
        cY = int(M["m01"] / M["m00"]) / gray.shape[0]
        return [cX, cY]