# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 10:13:11 2017

@author: EAmankwah
"""

def merge(line):
     # Helper function that merges a single row or column in 2048
     # Move all non-zero values of list to the left
     nonzeros_removed = []
     result = []
     merged = False
     for number in line:
         if number != 0:
             nonzeros_removed.append(number)
 
 
     while len(nonzeros_removed) != len(line):
         nonzeros_removed.append(0)

     # Double sequental tiles if same value
     for number in range(0, len(nonzeros_removed) - 1):
         if nonzeros_removed[number] == nonzeros_removed[number + 1] and merged == False:
             result.append(nonzeros_removed[number] * 2)
             merged = True
         elif nonzeros_removed[number] != nonzeros_removed[number + 1] and merged == False:
             result.append(nonzeros_removed[number])
         elif merged == True:
             merged = False

     if nonzeros_removed[-1] != 0 and merged == False:
         result.append(nonzeros_removed[-1])


     while len(result) != len(nonzeros_removed):
         result.append(0)


     return result

INITIAL_LIST = [2,2,2,2,2]
FINAL_LIST = merge(INITIAL_LIST)
print FINAL_LIST 
