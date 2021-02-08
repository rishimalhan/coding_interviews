import os
import sys
import img_utils

def find_phone(img_path=False,img=False):


if __name__=='__main__':
    if (len(sys.argv) < 2):
        print("Insufficient number of arguments provided.\
            Provide Path to the image. (e.g ./find_phone_test_iamges/0.jpg)")
    if not os.access(sys.argv[1], os.W_OK):
        print("Path Invalid")

    img_path = sys.argv[1]

    find_phone(img_path=img_path)