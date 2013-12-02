#!/usr/bin/python

#run example : ./scc.py add  --filename lol.c

import os,sys
import sys, getopt
import pickle
import time
import datetime
import diff_match_patch

sys.stderr = sys.stdout

""" Constant defining the number of commits before a full copy
of the file is saved (for efficiency)
"""
full_save_index  = 5

class Command():
    def __init__(self,params):
        self.params = params

###################################################################
#               Helper Functions
###################################################################


    """branch - Which branch to switch to
    writes the desired branch to a file called branch
    """
    def __write_branch(self,branch):
        filename = self.params['filename']
        my_path = ".scc/"+filename+".info/"
        my_file = open(my_path + "branch",'w')
        my_file.write(branch)
        my_file.close()

    """ Returns the name of the current branch for the given filename
    """
    def __get_current_branch(self, filename):
        fileDirPath = ".scc/"+filename+".info/"

        branchFile = open(fileDirPath + "branch",'r')
        branchName = branchFile.read()
        branchFile.close()

        return branchName

    """ Returns the version data consisting of a list of dictionaries
    for the given filename and branch
    """
    def __read_version_data(self,filename,branch):
        branchPath = ".scc/" + filename + ".info/" + branch + "/"

        versionFile = open(branchPath + "version",'r')
        data = pickle.load(versionFile)
        versionFile.close()

        """ Pickle may convert the list to a dict if the list has only
        one item, so convert it back to a list if this happens
        """
        if (type(data) == dict):
            data = [data]

        return data

    """ Writes the version data consisting of a list of dictionaries
    for the given filename and branch
    """
    def __write_version_data(self,filename,branch,data):
        branchPath = ".scc/" + filename + ".info/" + branch + "/"

        versionFile = open(branchPath + "version", 'w')
        pickle.dump(data, versionFile)
        versionFile.close()

    """ Reconstructs the contents of a file of a given version
    by applying the patches one at a time
    """
    def __reconstruct_version_content(self,filename,branch,requestedVersion):
        versionData = self.__read_version_data(filename, branch)

        # Find the last version that contained the full content
        for versionInfo in reversed(versionData[:requestedVersion]):
            if versionInfo["isDiff"] == False:
                lastFullVersion = int(versionInfo["version"])
                break

        branchPath = ".scc/" + filename + ".info/" + branch + "/"

        # Check if the version requested already contains the full content
        if requestedVersion == lastFullVersion:
            # Fetch the full content
            fullFile = open(branchPath + str(lastFullVersion),'r')
            contents = fullFile.read();
            fullFile.close()
        else:
            # Reconstruct the full content using the diffs
            initialFile = open(branchPath + str(lastFullVersion),'r')
            contents = initialFile.read();
            initialFile.close()

            diff = diff_match_patch.diff_match_patch();

            # Apply the patches one by one
            for i in range(lastFullVersion + 1, requestedVersion + 1):
                patchFile = open(branchPath + str(i),'r')
                patch = pickle.load(patchFile)
                patchFile.close()

                contents = diff.patch_apply(patch, contents)[0]

        return contents


    """branch - which branch the file should be created in
    Creates the file in the specified branch,and sets its version to 1
    """
    def __create_file(self,branch):
        filename = self.params['filename']
        my_path = ".scc/"+filename+".info/"+branch+"/"
        os.system("mkdir -p " +my_path)

        versionData = [{ "version": 1, "comment": "First commit", "time": datetime.datetime.now(),
                         "isDiff": False }]
        self.__write_version_data(filename, branch, versionData)

        #since this is the time the file is added , copy the whole file as version 1
        os.system("cp "+filename + " "+my_path+"1")

    """ Returns whether the file has been added to the repository before or not
    """
    def __file_in_repository(self, filename):
        my_path = ".scc/"+filename+".info/"
        if(os.path.exists(my_path)):
            return True
        else:
            return False

    """Branch - Which branch to check for
    Returns True if the file has been added/branched before
    False otherwise
    """
    def __branch_exists(self,branch):
        filename = self.params['filename']
        my_path = ".scc/"+filename+".info/"+branch
        if(os.path.exists(my_path)):
            return True
        else:
            return False


    """command - the command for which to check arguments
    Retrurns True if the right arguments are supplied for the command
    False if incorrect Arguments are supplied,or extra arguments are supplied
    """
    def check_args(self,command):
        args = {'add'           : ['filename'],
                'checkin'       : ['filename','comment'],
                'checkout'      : ['filename','version'],
                'checkout'      : ['filename'],
                'list'          : ['filename'],
                'list_branches' : ['filename'],
                'branch'        : ['filename','branch'],
                'merge'         : ['filename','branch','to_branch'],
                'switch'        : ['filename','branch'],
                }
        num_args = 0
        for  arg in args[command]:
            #make sure the right args are specified
            if not arg in self.params:
                print "Error: argument "+arg+" required"
                sys.exit(1)
            num_args = num_args + 1


###################################################################
#               Primary Functions
###################################################################


    """command - which version control command to execute
    execute will run the command specified
    """
    def execute(self,command):
        #getattr gets a function of this class with name == command
        getattr(self, command)()

    """adds tracking for the current file at version 1
    will terminate program if the file exists
    """
    def add(self):
        #Check if we have info for the file already
        if(self.__branch_exists("main")):
            print "Error: file: "+self.params['filename'] +" already added"
            sys.exit(1)
        self.__create_file("main")
        #set the branch of the file to main
        self.__write_branch("main")
        print "Added file '" + self.params['filename'] + "' at version 1"

    """creates a new branch for the program
    will terminate program if the file exists
    """
    def branch(self):
        branch =  self.params['branch'];
        filename =  self.params['filename'];
        if(self.__branch_exists(branch)):
            print "Error: branch '%s' already created" % branch
            sys.exit(1)
        # Make sure file exists under source control
        if not self.__file_in_repository(filename):
            print "Error: file: '%s' is not in source code control" % filename
            return
        self.__create_file(branch)
        print "Branch '%s' created" % branch

    """switches the branch for the file given
    will terminate if the branch doesn't exist
    """
    def switch(self):
        filename = self.params['filename']
        branch = self.params['branch']
        #Check to see if the branch exists
        if not self.__branch_exists(branch):
            print "Error: Can't switch to non-existant branch: '%s'" % branch
            sys.exit(1)
        #Don't do anyhting if we are already on the branch
        if self.__get_current_branch(filename) == branch :
            print "Doing nothing, already on branch '%s'" % branch
            return
        #update the branch file to switch the branch
        self.__write_branch(self.params['branch'])
        #checkout the most recent version of the file on branch
        versionData = self.__read_version_data(filename, branch)
        version = versionData[-1]["version"]

        # Get the content and write it out
        content = self.__reconstruct_version_content(filename, branch, version)

        curFile = open(filename, 'w')
        curFile.write(content)
        curFile.close()
        print "Switched to branch '%s'" % branch

    """ Checks in the file to the repository
    """
    def checkin(self):
        filename = self.params['filename']

        # Make sure file exists under source control
        if not self.__file_in_repository(filename):
            print "Error: file: '"+filename+"' not under source control"
            return

        branch = self.__get_current_branch(filename)
        comment = self.params['comment']

        # Get the version data for the file
        versionData = self.__read_version_data(filename, branch)

        lastVersion = versionData[-1]["version"]
        newVersion = lastVersion + 1

        # Compute the diffs between the file in the repository and the current file
        previousContent = self.__reconstruct_version_content(filename, branch, lastVersion)

        curFile = open(filename, 'r')
        newContent = curFile.read()
        curFile.close()

        diff = diff_match_patch.diff_match_patch()
        patch = diff.patch_make(previousContent, newContent)

        # Make sure the files are actually different
        if not patch:
            print "No diffs found, repository already contains latest version"
            return

        branchPath = ".scc/" + filename + ".info/" + branch + "/"
        contentsFile = open(branchPath + str(newVersion), 'w')

        # Check whether we should save a full copy or only the diffs
        if ((newVersion - 1) % full_save_index) == 0:
            # Save a full copy
            contentsFile.write(newContent)

            isDiff = False
        else:
            # Save the diffs
            pickle.dump(patch, contentsFile);

            isDiff = True

        contentsFile.close()

        # Create the new version entry
        versionEntry = { "version": newVersion, "comment": comment, "time": datetime.datetime.now(),
                         "isDiff": isDiff }
        versionData.append(versionEntry)

        self.__write_version_data(filename, branch, versionData)

        print "Checked in version " + str(newVersion) + " with comment '" + comment + "'"

    """ checks a specific version of a file out of the repository
    if there is no version specified, gets the latest version
    """
    def checkout(self):
        filename = self.params['filename']

        # Make sure file exists under source control
        if not self.__file_in_repository(filename):
            print "Error: file not under source control"
            return

        branch = self.__get_current_branch(filename)

        # Get the latest version
        versionData = self.__read_version_data(filename, branch)
        lastVersion = versionData[-1]["version"]

        # Check if version was input as parameter
        if 'version' in self.params:
            version = int(self.params['version'])
        # If it wasn't, use latest version
        else:
            version = lastVersion

        # Make sure version is within bounds
        if version > lastVersion or version < 1:
            print "Error: version number is out of bounds"
            return

        # Get the content and write it out
        content = self.__reconstruct_version_content(filename, branch, version)

        curFile = open(filename, 'w')
        curFile.write(content)
        curFile.close()

        print "Checked out version " + str(version) + " of file '" + filename + \
              "' from branch '" + branch + "'"

    """ Creates a file containing the suggested merge for two different branches.
    Returns an error if no simple merge is possible
    """
    def merge(self):
        filename = self.params['filename']
        from_branch = self.params['branch']
        to_branch = self.params['to_branch']

        #make sure both branches exist
        if not self.__branch_exists(from_branch):
            print "Error: Branch '%s' does not exist" % from_branch
            return
        if not self.__branch_exists(to_branch):
            print "Error: Branch '%s' does not exist" % to_branch
            return

        #get the previous and current version file in the source branch
        version_data = self.__read_version_data(filename, from_branch)
        curr_version = version_data[-1]["version"]
        prev_version = curr_version - 1

        #Make sure the branch has an update
        if prev_version < 1:
            print "Error: Cannot suggest merge on a newly branched file"
            return

        #diff the two versions to isolate the last change in a patch
        prev_content = self.__reconstruct_version_content(filename, from_branch, prev_version)
        curr_content = self.__reconstruct_version_content(filename, from_branch, curr_version)

        diff =  diff_match_patch.diff_match_patch()
        patch = diff.patch_make(prev_content, curr_content)

        #get the contents of the file in the to_branch
        version_data = self.__read_version_data(filename, to_branch)
        curr_version = version_data[-1]["version"]
        content = self.__reconstruct_version_content(filename, to_branch, curr_version)

        #patch the file in the latest to branch,and store if it suceeded
        content,sucessful= diff.patch_apply(patch, content)

        #Tell the user we couldn't patch if the merge failed
        if not sucessful[0]:
            print "Error: Unable to merge branches, branch files too different"
            return

        #write out the suggested file as filename.suggested
        suggested_file = open(filename + ".suggested",'w')
        suggested_file.write(content)
        suggested_file.close()

        print "Merged branch %s to best resemble update in branch %s" %( to_branch, from_branch)
        print "Wrote out suggested merge in %s.suggested" % filename

    """ Lists all of the versions (with comments) and time associated with a file
    in the current branch
    """
    def list(self):
        filename = self.params['filename']

        # Make sure file exists under source control
        if not self.__file_in_repository(filename):
            print "Error: file not under source control"
            return

        branch = self.__get_current_branch(filename)

        print "Listing versions for '" + filename + "' in branch '" + branch + "'\n"

        # Get the version data and print its contents
        data = self.__read_version_data(filename, branch)
        for version in data:
            print "Version " + str(version["version"])
            print "    Comment: " + version["comment"]
            #print "\tDate: " + version["time"].strftime("%c")

    """ Lists all of the different branches that exist for a file
    Branch names are the same as the folder names in  the directory
    containing the metadata for a file
    """
    def list_branches(self):
        filename = self.params['filename']

        # Make sure file exists under source control
        if not self.__file_in_repository(filename):
            print "Error: file not under source control"
            return

        # Set the path to the folder where all the branches are saved
        path = ".scc/" + filename + ".info/"

        # Print out all of the directory names, i.e. branches
        #os.system("ls %s -F | grep /") % path
        #for filename in os.listdir(path):
        print os.walk(path).next()[1]


def main(argv):
    #remove our command out of the arguments and save it
    command = argv.pop(0)
    #make sure we have a valid command
    if not command in ("add","branch","merge","checkin", \
            "checkout","list","switch", "list_branches"):
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
    commandObj.check_args(command)
    commandObj.execute(command)

if __name__ == "__main__":
    main(sys.argv[1:])
