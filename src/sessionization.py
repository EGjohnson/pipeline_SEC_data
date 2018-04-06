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
import gc
#os.chdir('~/PetGit/pipeline_SEC_data/input') # Provide the path here
print os.getcwd() # Prints the working directory
datapath='/home/ej/PetGit/pipeline_SEC_data/input/log.csv'
fh = open(datapath, 'r')
location_checked=[]
the_split=[]
cs={} #dictionary of current sessions
error_rec=[]
#functions
#===================================================================
check_len = lambda x: len(x)==15
no_blank=lambda x: '' not in x[0:3]+x[4:7]
no_space=lambda x: ' ' not in x[0:3]+x[4:7]
ip_lapsed=lambda tups,e,t: set([x[0] for x in tups if x[1]+e<t])

#....................................................................
def check_field_length(lx,i): #takes in raw line
    if len(lx)!=15 and len(lx)>0:
        return False
    else:
        return True
    
 
def convert_datetime(lx,i):
        dts=str(lx[1])+str(",")+str(lx[2]) #date time string
        dto=datetime.strptime(dts,'%Y-%m-%d,%H:%M:%S') #date time object
        return dto

def convert_unique_doc_request(lx,i):
        udr=str(lx[4])+str(lx[5])+str(lx[6]) #key unique doc request
        return udr


    
    
    #input elapsed time and tuples of live sessions
    

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
    #print '-----------'*2
    #print line_split
    #print "line split length: ", len(line_split)
    
    
    
     #1. If nothing has been written, wait two seconds and look again
    #==============================================================
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    if not line:
        error_rec.append("L"+str(i)+" no line")
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
    #print "begin processing line"
    
    # a. verify we do not have a truncated line, else give up
    #--------------------------------------------------------------
    if check_field_length(line_split,i)==True:
        pass
    else:
        error_rec.append("L"+str(i)+" truncated line missing fields")
        continue
    
    # b. verify we do not have blank fields, else give up
    #--------------------------------------------------------------
    if no_blank(line_split)==True and no_space(line_split)==True:
        pass
    else:
        error_rec.append("L"+str(i)+" blank or space in field")
        continue
    
    # c. attempt to create datetime object from fields, else give up
    #--------------------------------------------------------------
    try:
        dto=convert_datetime(line_split,i) #make datetime object from fields
    except Exception as e:
        error_rec.append("L"+str(i)+" convert_datetime error: " +str(e))
        continue
    
    # d. attempt to create unique doc request key, else give up
    #--------------------------------------------------------------
    try:
        urk=convert_unique_doc_request(line_split,i) #unique request key
    except Exception as e:
        error_rec.append("L"+str(i)+" convert_unique_doc_request error: " +str(e))
        continue
    
    
    # 4. Now add to dictionary object of current sessions
    #------------------------------------------------------------------
    #ip address, time of 1st request, time of 2nd request, duration, count requests
    cs[line_split[0]+str(i)]=(dto,line_split[0],urk+str(i)) # add datetime and ip and access record
    #session  time1stdoc-timelastdoc+elapsedtime
    #duration time1stdoc-timelastdoc
    
    
 
gc.collect() 
fh.seek(0)   #reset
    
