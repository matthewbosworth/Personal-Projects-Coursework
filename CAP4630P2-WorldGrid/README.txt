CAP 4630 Project 2 - Path Finder in Grid World

# Running the program

1. Navigate to the directory where you saved the folder
2. Run - python search.py (python 3.11 was used for this project)

After running the program, you should see 4 .png files that are plots for each world, 
showing the path found by each algorithm. 
The path cost and number of nodes expanded will be printed in the console, 
but are also provided in summary.txt for reference per project requirements.
You will see an additional 4 .png files that start with world2 that show the paths 
found by each algorithm for world 2 (my own test case).
Note: summary.txt only contains the results for world 1 (the provided test case) because it was
not required to include a summary for my own test case, per project requirements.

# Files - Purpose 
grid.py - provided point class
utils.py - provded stack, queue, and priority queue classes
search.py - main program that implements the search algorithms and draws the plots
TestingGrid/world1_enclosures.txt - provided test case enclosures
TestingGrid/world1_turfs.txt - provided test case turfs
TestingGrid/world2_enclosures.txt - my own test case enclosures
TestingGrid/world2_turfs.txt - my own test case turfs
TestingGrid/astar_result.png - plot of A* path for world 1
TestingGrid/bfs_result.png - plot of BFS path for world 1
TestingGrid/dfs_result.png - plot of DFS path for world 1
TestingGrid/gbfs_result.png - plot of GBFS path for world 1
TestingGrid/world2_astar_result.png - plot of A* path for world 2
TestingGrid/world2_bfs_result.png - plot of BFS path for world 2
TestingGrid/world2_dfs_result.png - plot of DFS path for world 2
TestingGrid/world2_gbfs_result.png - plot of GBFS path for world 2
summary.txt - summary of results for world 1 (provided test case) per project requirements
README.txt - this file, which provides instructions for running the program and descriptions of the project files

Note: If you would like to see the program generate fresh plots, 
you can delete the .png files in the TestingGrid folder and re-run the program.