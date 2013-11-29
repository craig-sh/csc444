#!/usr/bin/python

#run example : ./scc.py add  --filename lol.c

import os,sys
import sys, getopt 


def add(params):
    #TODO Check if file exists 
    filename = params['filename']
    #Make the directory structure for the file
    my_path = ".scc/"+filename+".info/main/"
    os.system("mkdir -p " +my_path)
    #create and write the version file
    my_file = open(my_path + "version",'w')
    my_file.write('1 File Added\n')
    my_file.close()
    #since this is the time the file is added , copy the whole file as version 1
    os.system("cp "+filename + " "+my_path+"1")

def branch(params):
    print "TODO Branch " + params['branch']
def checkin(params):
    print "TODO checkin " + params['filename'] + " " + params['comment']
def checkout(params):
    print "TODO checkout " + params['filename'] + " " + params['version']
def merge(params):
    print "TODO merge " + " " +  params['filename'] + " " + params['branch'] +" " + params['to_branch'] 
def list(params):
    print "TODO merge " + params['filename']
def switch(params):
    print "TODO merge " + params['filename'] +" "+ params['branch']

def main(argv):
    #remove our command out of the arguments and save it 
    command = argv.pop(0)
    #make sure we have a valid command
    if not command in ("add","branch","merge","checkin","checkout","list"):
        sys.exit("Invalid command " + command)
    try:
        opts, args = getopt.getopt(argv,"hf:c:v:b:t:s:",["filename=",
        "comment=","version=","branch=","to_branch=","--switch"])

    except getopt.GetoptError:
        print 'Input Error'
        sys.exit(1)
    #fill the parameters
    params = {}
    for opt,arg in opts:
        if opt in ("-f","--filename"):
            params['filename'] = arg 
        elif opt in ("-c","--comment"):    
            params['comment'] = arg 
        elif opt in ("-v","--version"):    
            params['version'] = arg 
        elif opt in ("-b","--branch"):    
            params['branch'] = arg 
        elif opt in ("-t","--to_branch"):    
            params['to_branch'] = arg 
        elif opt in ("-s","--switch"):    
            params['to_branch'] = arg 

    #call the apporpriate command with the arguments
    eval(command+"(params)")

if __name__ == "__main__":
   main(sys.argv[1:])
