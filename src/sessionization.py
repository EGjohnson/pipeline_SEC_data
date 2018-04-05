# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 15:05:46 2018

@author: ej
"""

"""    
    # process entry ID error --------------------------------------
    if check_len(line_split)!=15:
           fh.readline()
           continue
    convert_datetime(line_split,i)
#    except (TypeError, NameError,ValueError):
#         print "Warning: DateTime Format Error line: "+str(i)
#         #normally I would write to an error log
#         continue
"""
import os
import time
from datetime import datetime
#os.chdir('~/PetGit/pipeline_SEC_data/input') # Provide the path here
print os.getcwd() # Prints the working directory
datapath='/home/ej/PetGit/pipeline_SEC_data/input/log_trunct_lines.csv'
fh = open(datapath, 'r')
location_checked=[]
the_split=[]
#functions
#===================================================================
check_len = lambda x: len(x)==15
grab_dat=lambda x: x[0:3]+x[4:7]



#....................................................................
def check_field_length(lx,i): #takes in raw line
    if len(line_split)!=15 and len(line_split)>0:
        print "check_field_length error: not enough fields!"
        return False
    else:
        return True
 
def convert_datetime(lx,i):
    try:
        dts=str(lx[1])+str(",")+str(lx[2]) #date time string
        dto=datetime.strptime(dts,'%Y-%m-%d,%H:%M:%S') #date time object
        return dto
    except Exception as e:
        print "convert_datetime error for line: " +str(i)
        return e
        
    
#................................................................
         
#buffer past header
fh.seek(0)
fh.readline()
fh.seek(fh.tell())
i=1

while True:
    print(i)
    i=i+1
    # Check to see if a new line has been written
    #================================================================
    try_this_line=fh.tell() # bookmark line
    #fh.seek(try_this_line) #resets to beginning
    line=fh.readline() # content written on this line
    line_split=line.split(',')
    check_len(line_split)
    the_split.append(line_split)
    print '-----------'*2
    print line_split
    print "line split length: ", len(line_split)
    
    
    
     #1. If nothing has been written, wait two seconds and look again
    #==============================================================
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    if not line:
        print "no line!"
        time.sleep(5) # wait five seconds
        fh.seek(try_this_line) #reset back to the same line and check again
      
        location_checked.append(try_this_line) #moniter how long checkings same line
        if set(location_checked)>1: # if checking new line now reset moniter
            location_checked=[]
            
        
    #2. If nothing has been written for 30 seconds halt the script
    #============================================================== 
        if location_checked>6:
            print "STREAMING HAS HALTED"
            break
        
        continue
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    # 3. Otherwise process the line
    #=============================================================
    print "begin processing line"
    # Process entry ----------------------------------------------
    
    # a. verify we do not have a truncated line
    if check_field_length(line_split,i)==True:
        pass
    else:
        continue
    
    
    # b. verify we can generate a dattime object from fields

#    if len(line_split)!=15 and len(line_split)>0:
#        print "entry too short!"

    
