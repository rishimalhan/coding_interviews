#import necessary libraries
import sys
import numpy as np
import cv2
import imutils
import glob
import pandas as pd


#save user input image file
data_path = str(sys.argv[1])
# labels = np.array(pd.read_csv( data_path + "/labels.txt",header=None,sep=' ' ))

y_var = np.array([])
# Print png images in folder C:\Users\admin\
for image_file in glob.iglob(data_path+'/obj_detection/contour_based/detect/'+'/*.jpg'):
	#load image and convert to grayscale
	image = cv2.imread(image_file)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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
		print("0.5 0.5")

	#else, contour "algorithm" to detect phone contour
	else:
		cnts_values = np.ones(N)*np.maximum(image.shape[0],image.shape[1])
		for i in range(N):
		    param = cv2.arcLength(cnts[i],True)/4
		    area = np.sqrt(cv2.contourArea(cnts[i]))
		    if (param>10) and (area>10):
		        cnts_values[i] = np.absolute(param-area)/np.minimum(param,area)
		phone = np.argmin(cnts_values)

		#calculate and print center
		M = cv2.moments(cnts[phone])
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		np.append( y_var, np.array([cX/image.shape[1],cY/image.shape[0]]) )
		print(str(cX/image.shape[1]) + ' ' + str(cY/image.shape[0]))
print( y_var )