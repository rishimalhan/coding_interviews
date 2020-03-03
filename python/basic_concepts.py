import random
import copy
import pandas as pd
import numpy as np


# Strings in python
str_1 = "mystring"
for i in range(0,len(str_1)):
    print(str_1[i])


# Declaration of an array with some initialized value
size = 10
val = 1
arr = [val]*size
print(arr)

# Testing uneven number of elements in a list
py_list = [ [1,2,3],[4,5] ]
print(py_list)



letter = 'a'
alph_list = []
for i in range(0,26):
    alph_list.append(letter)
    letter = chr(ord(letter)+1)

print(alph_list)
print(random.choice(alph_list))
print(alph_list.index('a'))
print(10%2)


print("\n\n")


# # write your code in Python 3.6
# soltn_string = []
# # Generate a list of 26 alphabets
# letter = 'a'
# alph_list = []
# for i in range(0,26):
#   alph_list.append(letter)
#   letter = chr(ord(letter)+1)

# # occurence list maintains how many times a letter has occurred
# occ_list = [0]*26

# # Pick character at random and append it once to solution if odd else twice
# while (len(soltn_string)!=4):
#   print("Appending")
#   ran_lett = random.choice(alph_list)
#   if (occ_list[alph_list.index(ran_lett)]%2==0): # Even
#       soltn_string.append(ran_lett)
#       occ_list[alph_list.index(ran_lett)] += 1
#   else:
#       soltn_string.append(ran_lett)
#       soltn_string.append(ran_lett)
#       occ_list[alph_list.index(ran_lett)] += 2


# print(soltn_string)


print("\n\n")

print(5>float("-inf"))

a = [1,1,2,3,4]
while(a.count(1)!=0):
    a.remove(1)

print(a)



def change_val(a):
    a = copy.deepcopy(a)
    while(a.count(1)!=0):
        a.remove(1)
a = [1,1,1,2,3,4]
change_val(a)
print(a)

