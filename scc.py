#!/usr/bin/python

#run example : ./scc.py add  --filename lol.c

import os,sys
import sys, getopt 
sys.stderr = sys.stdout

class Command():
    def __init__(self,params):
        self.params = params
                
    def execute(self,command):
        #getattr gets a function of this class with name == command
        getattr(self, command)()
    def create_file(self,branch,filename):
        my_path = ".scc/"+filename+".info/"+branch+"/"
        os.system("mkdir -p " +my_path)
        #TODO change the version stuff to match Edmunds checkin/checkout funtions
        my_file = open(my_path + "version",'w')
        my_file.write('1 File Added\n')
        my_file.close()
        #since this is the time the file is added , copy the whole file as version 1
        os.system("cp "+filename + " "+my_path+"1")

    def add(self):
        #TODO Check if file exists 
        filename = self.params['filename']
        self.create_file("main",filename)   

    def branch(self):
        #TODO Check if file exists 
        branch =  self.params['branch']
        create_file(branch,filename)   
    def checkin(self):
        print "TODO checkin " + self.params['filename'] + " " + self.params['comment']
    def checkout(self):
        print "TODO checkout " + self.params['filename'] + " " + self.params['version']
    def merge(self):
        print "TODO merge " + " " +  self.params['filename'] + " " + self.params['branch'] +" " + self.params['to_branch'] 
    def list(self):
        print "TODO merge " + self.params['filename']
    def switch(self):
        print "TODO merge " + self.params['filename'] +" "+ self.params['branch']

def main(argv):
    #remove our command out of the arguments and save it 
    command = argv.pop(0)
    #make sure we have a valid command
    if not command in ("add","branch","merge","checkin","checkout","list","switch"):
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
    commandObj = Command(params)      
    commandObj.execute(command)

if __name__ == "__main__":
    main(sys.argv[1:])
