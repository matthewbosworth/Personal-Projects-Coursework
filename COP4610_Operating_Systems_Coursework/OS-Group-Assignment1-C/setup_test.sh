#!/bin/bash
# Test setup script for DOS Command Interpreter demonstration

echo "Setting up test environment for DOS Command Interpreter..."

# Create a test directory structure
mkdir -p test_demo
cd test_demo

# Create test subdirectories
mkdir -p subdir1 subdir2

# Create test files with content
echo "This is test file 1" > testfile1.txt
echo "This is test file 2" > testfile2.txt
echo "Sample content for copying" > source.txt
echo "File to be renamed" > oldname.txt
echo "File to be deleted" > todelete.txt

# Create a file in subdirectory
echo "File in subdirectory" > subdir1/subfile.txt

echo ""
echo "Test environment created in test_demo/"
echo ""
echo "Directory structure:"
tree test_demo/ 2>/dev/null || find test_demo/ -print
echo ""
echo "You can now test the following scenarios:"
echo ""
echo "1. cd command:"
echo "   DOS> cd test_demo"
echo "   DOS> pwd"
echo "   DOS> cd .."
echo ""
echo "2. dir command:"
echo "   DOS> dir"
echo "   DOS> dir test_demo"
echo ""
echo "3. type command:"
echo "   DOS> type test_demo/testfile1.txt"
echo ""
echo "4. copy command:"
echo "   DOS> copy test_demo/source.txt test_demo/destination.txt"
echo "   DOS> dir test_demo"
echo ""
echo "5. ren command:"
echo "   DOS> ren test_demo/oldname.txt test_demo/newname.txt"
echo "   DOS> dir test_demo"
echo ""
echo "6. del command:"
echo "   DOS> del test_demo/todelete.txt"
echo "   DOS> dir test_demo"
echo ""
echo "7. Error cases:"
echo "   DOS> cd"
echo "   DOS> copy onefile.txt"
echo "   DOS> cd too many arguments"
echo ""
echo "Setup complete! Run ./dos_interpreter to start testing."
