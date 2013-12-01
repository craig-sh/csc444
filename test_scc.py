import os,sys
import sys, getopt
from subprocess import call

#To run: python test_scc.py

def validate(test_num, test):

    # Set the paths for the test files
    output_path = "Test_Actual_Results/Test%d.txt" %test_num
    expected_path = "Test_Expected_Results/Test%d.txt" %test_num

    # Make a call to the scc program with the desired test conditions
    # saving the results to a text file in the output path
    os.system(test + " > " + output_path)

    # Open the outputted file and expected results for comparison
    expected_results_file  = open(expected_path, 'r')
    actual_results_file = open(output_path, 'r')

    # Read the information contained in the files
    expected_results = expected_results_file.readlines()
    actual_results = actual_results_file.readlines()

    # Print the results based on whether the results match the expected
    if (expected_results == actual_results):
        print "Test %d: Passed" % test_num
        print "	Command Run: " + test

    else:
        print "Test %d: Failed" % test_num
	print "	Command Run: " + test
        print "	Expected Results: " + str(expected_results)
        print "	Actual Results: " + str(actual_results)

    # Close the files and return
    expected_results_file.close()
    actual_results_file.close()

def main():

    # Set up files for testing in main directory
    os.system("cp Test_Input_Files/*.test .")

    test_number = 1

    """ Run tests on command parsing """

    # Test1: Invalid command
    test_case = "python scc.py fake_command"
    validate (test_number, test_case)
    test_number += 1

    # Test2: Missing arguments
    test_case = "python scc.py checkin"
    validate (test_number, test_case)
    test_number += 1

    """ Run tests on add """

    # Test3: Add a file to be tracked
    test_case = "python scc.py add -f a.test"
    validate (test_number, test_case)
    test_number += 1

    # Test4: Add a file to be tracked that's been added before
    test_case = "python scc.py add -f a.test"
    validate (test_number, test_case)
    test_number += 1

    """ Run tests on branch """

    # Test5: Branch a file that's been added
    test_case = "python scc.py branch -f a.test -b test_branch"
    validate (test_number, test_case)
    test_number += 1

    # Test6: Recreate branch that exists
    test_case = "python scc.py branch -f a.test -b test_branch"
    validate (test_number, test_case)
    test_number += 1

    # Test7: Branch a file that does not exist
    test_case = "python scc.py branch -f z.test -b test_branch2"
    validate (test_number, test_case)
    test_number += 1

    """ Run tests on switch """

    # Test8: Switch to a branch that exists for a file that exists
    test_case = "python scc.py switch -f a.test -b test_branch"
    validate (test_number, test_case)
    test_number += 1

    # Test9: Switch to branch that does not exist
    test_case = "python scc.py switch -f a.test -b test_branch2"
    validate (test_number, test_case)
    test_number += 1

    # Test10: Switch to branch that you are already in
    test_case = "python scc.py switch -f a.test -b test_branch"
    validate (test_number, test_case)
    test_number += 1

    """ Run tests on checkin """

    # Test11: Check in file not under source control
    test_case = "python scc.py checkin -f b.test -c 'file does not exist'"
    validate (test_number, test_case)
    test_number += 1

    # Test12: Check in file with no changes, i.e. latest version
    test_case = "python scc.py checkin -f a.test -c 'version 2'"
    validate (test_number, test_case)
    test_number += 1

    # Write changes to file a.test before proceeding with next test
    os.system("echo 'This is a newline' >> a.test")
    #test = raw_input()

    # Test13: Check in file with changes (this is on the new_branch)
    test_case = "python scc.py checkin -f a.test -c 'version 2'"
    validate (test_number, test_case)
    test_number += 1

    """ Run tests on checkout """

    # Test14: Check out file that doesn't exist
    test_case = "python scc.py checkout -f z.test"
    validate (test_number, test_case)
    test_number += 1

    # Test15: Check out version that doesn't exist
    test_case = "python scc.py checkout -f a.test -v 3"
    validate (test_number, test_case)
    test_number += 1

    # Test16: Check out file -> version 1
    test_case = "python scc.py checkout -f a.test -v 1"
    validate (test_number, test_case)
    test_number += 1

    # Test17: Check out latest version
    test_case = "python scc.py checkout -f a.test"
    validate (test_number, test_case)
    test_number += 1

    """ Run tests on list """

    # Test18: List a file that doesn't exist
    test_case = "python scc.py list -f z.test"
    validate (test_number, test_case)
    test_number += 1

    # Test19: List a file in the current branch (on version 2)
    test_case = "python scc.py list -f a.test"
    validate (test_number, test_case)
    test_number += 1

    # switch to main branch in order to list
    os.system("python scc.py switch -f a.test -b main > temp.test")

    # Test20: List a file in the main branch (unchanged)
    test_case = "python scc.py list -f a.test"
    validate (test_number, test_case)
    test_number += 1

    """ Run tests on merge """

    """ Remove test files from main directory """
    os.system("rm *.test")
    os.system("rm -rf .scc")

if __name__ == "__main__":
    main()
