csc444
======

CSC444'13 Assignment 2

Due December 2nd at Start of Class

The purpose of this assignment is for you to develop an awareness of issues regarding the use and implementation of source code control systems.
You may work in teams of up to three people.
Design and develop a simple command-line source code control system. 

The system should be capable of satisfying the following requirements.
Handle ASCII text files only.
Put a file under source code control.
Check in a modified version of a file after the user edits it.
Allow the user to associate a comment with each check-in.
Assign version numbers to all check-ins.
Check out the most current version of a file.
Check out any older version of a file by version number.
List all versions of a file with their associated check-in comment.
Create a new source control branch for a file associating a unique user-chosen identifier with the new branch (the original branch should be called "main").
All of the above requirements should be satisfyable equally for all branches.
Generate a suggested file as the next version for branch X based on the last change applied to branch Y (where X and Y can be any non-equal branch names).


Hand in:
A specification document describing your command-line design (20%).
Includes 5% on perceived usability.
A design document explaining the major implementation decisions (20%).
Includes 5% on perceived effiiciency (as validated in the code), and 5% on the quality of the algorithm for suggesting a change to branch X given a change in branch Y.
Source code for your system (40%)
Comprising source code modularity and design (20%) and readability/coding/commenting style (20%).
Test cases, expected results, and actual results (20%).
