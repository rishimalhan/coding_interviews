""" This module is used to find coordinates of the phone in the image."""

# Loading dependencies.
import os
import sys

# Data pre-processing libraries.
import cv2
import numpy as np

# Machine learning modelling libraries.
from keras.models import load_model

def find_phone(path):
    os.chdir(path)
    cwd = os.getcwd()
    label_data = []

    # Accessing data files.
    for file in os.listdir(cwd):
        if file.endswith(".txt"):
            with open("labels.txt") as file:
                for line in file:
                    data_line = [l.strip() for l in line.split(' ')]
                    label_data.append(data_line)

    # Processing Image files.
    x_variable = []
    y_variable = []
    for label in label_data:
        img = cv2.imread(label[0])
        resized_image = cv2.resize(img, (64, 64))
        x_variable.append(resized_image.tolist())
        y_variable.append([float(label[1]), float(label[2])])
    x_variable = np.asarray(x_variable)
    y_variable = np.asarray(y_variable)
    x_variable = np.interp(x_variable, (x_variable.min(), x_variable.max()), (0, 1))

    # Loading the Deep Learning Model.
    model = load_model('train_phone_finder_weights.h5')

    result = model.predict(x_variable)
    print( np.linalg.norm( (result-y_variable),axis=1 ) )

    # print( np.linalg.norm( result-y_variable, axis=1 ) )

    # print("\n\nPhone in image {0} is located at x-y coordinates given below."
    #       .format(str(file_name)))
    # print("\n{:.4f} {:.4f}".format(result[0][0], result[0][1]))

def main():
    """ This function is used to run the program. """
    find_phone(sys.argv[1])

if __name__ == "__main__":
    main()
