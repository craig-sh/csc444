import os,sys
import sys, getopt
from subprocess import call

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
    
    """ Run unit tests on command parsing """
     
    # Test 1: Invalid command 
    test_case = "python scc.py fake_command" 
    validate (test_number, test_case)
    test_number += 1
        
    # Test 2: Wrong number of arguments 

    test_case = "python scc.py checkin"
    validate (test_number, test_case)
    test_number += 1   
    
    # Test 3: 
    test_case = "python scc.py checkin -f a.test -c lol"
    validate (test_number, test_case)
    test_number += 1

    # Remove test files from main directory 
    os.system("rm *.test")

if __name__ == "__main__":
    main()
