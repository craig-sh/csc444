#!/usr/bin/python

#run example : ./scc.py add  --filename lol.c

import os,sys
import sys, getopt 
sys.stderr = sys.stdout

class Command():
    def __init__(self,params):
        self.params = params

###################################################################
#               Helper Functions
###################################################################

    
    #branch - Which branch to switch to 
    #writes the desired branch to a file called branch
    def write_branch(self,branch):
        filename = self.params['filename']
        my_path = ".scc/"+filename+".info/"
        my_file = open(my_path + "branch",'w')
        my_file.write(branch)
        my_file.close()


    #branch - which branch the file should be created in
    #Creates the file in the specified branch,and sets its version to 1
    def create_file(self,branch):
        filename = self.params['filename']
        my_path = ".scc/"+filename+".info/"+branch+"/"
        os.system("mkdir -p " +my_path)
        #TODO change the version stuff to match Edmunds checkin/checkout funtions
        my_file = open(my_path + "version",'w')
        my_file.write('1 File Added\n')
        my_file.close()
        #since this is the time the file is added , copy the whole file as version 1
        os.system("cp "+filename + " "+my_path+"1")

    #Branch - Which branch to check for
    #Returns True if the file has been added/branched before
    #False otherwise
    def file_tracking_exists(self,branch):
        filename = self.params['filename']
        my_path = ".scc/"+filename+".info/"+branch
        if(os.path.exists(my_path)):
            return True
        else:
            return False



###################################################################
#               Primary Functions
###################################################################


    #command - which version control command to execute
    #execute will run the command specified
    def execute(self,command):
        #getattr gets a function of this class with name == command
        getattr(self, command)()
    #adds tracking for the current file at version 1
    #will terminate program if the file exists
    def add(self):
        #Check if we have info for the file already
        if(self.file_tracking_exists("main")):
            print "Error: file: "+self.params['filename'] +" already added"
            sys.exit(1)
        self.create_file("main")
        #set the branch of the file to main
        self.write_branch("main")


    #creates a new branch for the program
    #will terminate program if the file exists
    def branch(self):
        if(self.file_tracking_exists(self.params['branch'])):
            print "Error: branch: " + self.params['branch'] + " already created"
            sys.exit(1)
        #TODO Check if file exists 
        branch =  self.params['branch']
        create_file(branch)

    #switches the branch for the file given
    #will terminate if the branch doesn't exist
    def switch(self):
        #Check to see if the branch exists 
        if not file_tracking_exists(self.params['branch']):
            print "Error: Can't switch to non-existant branch: " + params["branch"]
        #update the branch file to switch the branch
        self.write_branch(self.params['branch'])







    def checkin(self):
        print "TODO checkin " + self.params['filename'] + " " + self.params['comment']
    def checkout(self):
        print "TODO checkout " + self.params['filename'] + " " + self.params['version']
    def merge(self):
        print "TODO merge " + " " +  self.params['filename'] + " " + self.params['branch'] +" " + self.params['to_branch'] 
    def list(self):
        print "TODO list " + self.params['filename']


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
