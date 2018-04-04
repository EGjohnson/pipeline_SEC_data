# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 15:05:46 2018

@author: ej
"""
import os
import time
#os.chdir('~/PetGit/pipeline_SEC_data/input') # Provide the path here
print os.getcwd() # Prints the working directory
datapath='/home/ej/PetGit/pipeline_SEC_data/input/log.csv'
fh = open(datapath, 'r')
location_checked=[]
the_split=[]
#===================================================================

fh.seek(0)
header=fh.readline()

header = fh.readline() 

while True:
    # 1. See if a new line has been written
    #================================================================
    try_this_line=fh.tell() # check this line for new writes
    line=fh.readline(try_this_line) # content written on this line
    line_split=line.split(',')
    the_split.append(line_split)
    
    #2. If nothing has been written wait two seconds and look again
    #==============================================================
    if not line:
        print "no line!"
        time.sleep(5) # wait five seconds
        fh.seek(try_this_line) #reset back to the same line and check again

            
    #3. If nothing has been written for 30 seconds halt the script
    #==============================================================
            
        #----------------------------------------------------------
        location_checked.append(try_this_line) #moniter how long checkings same line
        if set(location_checked)>1: # if checking new line now reset moniter
            location_checked=[]
            
        #-----------------------------------------------------------
            
        if location_checked>6:
            print "STREAMING HAS HALTED"
            break
        continue
