# Project3 – README

## Overview
PrefAgent is a knowledge based intelligent system for solving preference problems.
It supports Penalty Logic and Qualitative Choice Logic (QCL) and performs
five reasoning tasks: Encoding, Feasibility Checking, Show Table, Exemplification,
and Omni-optimization.

## Run with
Python 3.11

## Directory Structure
Bosworth_Project3/
├── main.py                   
├── README.md
├── src/
│   ├── formula.py            
│   ├── parser.py           
│   ├── engine.py             
│   └── display.py            
├── ExampleTestCase/          
│   ├── attributes.txt
│   ├── constraints.txt
│   ├── penaltylogic.txt
│   └── qualitativechoicelogic.txt
└── TestCase/                
    ├── attributes.txt
    ├── constraints.txt
    ├── penaltylogic.txt
    └── qualitativechoicelogic.txt

## How to Run
From the project root directory:
python3.11 main.py

The system will prompt you for:
1. Attributes file path (e.g. `ExampleTestCase/attributes.txt`)
2. Hard constraints file path (e.g. `ExampleTestCase/constraints.txt`)
3. Choice of preference logic (Penalty Logic or QCL)
4. Preferences file path (e.g. `ExampleTestCase/penaltylogic.txt`)
5. Reasoning task to perform



