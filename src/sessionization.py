# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 15:05:46 2018

@author: ej
"""
import os
import csv
import time
from datetime import datetime
import gc
#os.chdir('~/PetGit/pipeline_SEC_data/input') # Provide the path here
print os.getcwd() # Prints the working directory
topdir=os.getcwd()[0:-4] #rmv source
#====================================================================
elapse_datpath=topdir+"/input/inactivity_period.txt"
f_elapse=open(elapse_datpath, 'r')
elapse=f_elapse.readline()
f_elapse.close()
elapse=2
datapath=topdir+'/input/log.csv'
fh = open(datapath, 'r')
datapath_out=topdir+'/output/sessionization.txt'
#=====================================================================
out_txt=open(datapath_out,'wb')
fw=csv.writer(out_txt)
location_checked=[]
the_split=[]
tups=[] #current sessions
error_rec=[]
#functions
#===================================================================
check_len = lambda x: len(x)==15
no_blank=lambda x: '' not in x[0:3]+x[4:7]
no_space=lambda x: ' ' not in x[0:3]+x[4:7]
grab_ip=lambda tups:set([x[0] for x in tups]) #graps unique ip for session
sub_ip=lambda tups,ip:[x for x in tups if x[0]==ip] #subset by ip
max_t_ip=lambda tups,ip:max([x[1] for x in tups if x[0]==ip]) #max time ip
session_elapsed=lambda ct,t,e: True if (ct-t).seconds>e else False #tests if time elapsed

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
        
def is_session_over(ip,tups,ct,e): 
    #ip tups current time and elapsed time allowed for session
    mt=max_t_ip(tups,ip) #last time accessed
    #print "last rec recorded-----------"
    #print mt
    tf=session_elapsed(ct,mt,e) #status of session 
    return tf

def group_to_entry(tups,ip):
    #subset group ands sort by time
    g=sub_ip(tups,ip)
    g.sort(key=lambda x: x[1])
    #find session duration
    g_dates=[e[1] for e in g] 
    g_tdiff=(max(g_dates)-min(g_dates)).seconds+1 
    #get count
    #len(g)
    #create string format for time
    min_t_str=g[0][3]+" "+g[0][4]
    max_t_str=g[len(g)-1][3]+" "+g[len(g)-1][4]
    #print min_t_str
    #print max_t_str
    #turn into string
    gstr=[ip,min_t_str,max_t_str,g_tdiff,len(g)]
    return gstr
    
    

def write_file(tups):
    grab_sec=lambda ts:float(ts[2][len(ts[2])-2:len(ts[2])])
    grab_sec2=lambda ts:float(ts[1][len(ts[1])-2:len(ts[1])])
    #sort by end time, presort by start time
    tups=sorted(tups,key=lambda ts:float(ts[2][len(ts[2])-2:len(ts[2])]))
    tups=sorted(tups,key=lambda ts:float(ts[1][len(ts[1])-2:len(ts[1])]))
    for wt in tups:
        #print ">>>>>>>>>> writing ips to file"
        #print wt
        fw.writerows([wt])
    
    
    #input elapsed time and tuples of live sessions
    

#................................................................
         
#buffer past header
fh.seek(0)
fh.readline()
fh.seek(fh.tell())
i=1

while True:
    #print(i)
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
            #write anything left down in the file
            #sort in exiting order
            ips_left=set([l[0] for l in tups ])
            write_lines=[group_to_entry(tups,ip) for ip in ips_left]
            #print write_lines
            if len(write_lines)>0:
                write_file(write_lines)
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
        error_rec.append("L"+str(i)+"convert_unique_doc_request error: " +str(e))
        continue
    
    
    # 4. Now add to current sessions
    #------------------------------------------------------------------
    #session  time1stdoc-timelastdoc+elapsedtime
    #duration time1stdoc-timelastdoc
  
    # 4a. update time ................................
    ct=dto #curent time
    #print ct
    # 4b. ID sessions are over .......................
    ips=grab_ip(tups)
    #print "the ips -----------------------"
    #print ips
    ips_over=[ip for ip in ips if is_session_over(ip,tups,ct,elapse)==True]
    #print " the ips sessions that are done ------"
    #print ips_over
    
    # 4c. write sessions that are over ..............
    #write_tups=[tup for tup in tups if tup[0] in ips_over]
    write_lines=[group_to_entry(tups,ip) for ip in ips_over]
    #print write_lines
    if len(write_lines)>0:
        write_file(write_lines)
 
    # 4d. remove sessions that are over..............
    #print "the new current sessions with old sessions removed -----"
    clean_tups=[tup for tup in tups if tup[0] not in ips_over]
    for mytup in clean_tups:
        #print mytup
        pass
    tups=clean_tups
   
    #print "--------------------------------------------------"
    
    
    
    tups.append((line_split[0],dto,urk+str(i),line_split[1],line_split[2])) # add datetime and ip and access record

    
    #ip address, time of 1st request, time of 2nd request, duration, count,requests
    
 
gc.collect() 
fh.seek(0)   #reset
out_txt.close()


