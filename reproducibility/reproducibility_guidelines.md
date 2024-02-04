# Reproducibility

[[TOC]]

The goal of this document is to identify the criteria used in VLDB and SIGMOD which pertains to a submission of a paper to the reproducibility track.

## SIGMOD definition

### Initial Observations

Initial observations indicate that SIDMOD has some clearly defined reproducibility guidelines outlined in [SIGMOD Guidelines](https://reproducibility.sigmod.org/#Guidelines)
In essence they are as follows:
1.	Define the environment (OS, HW) upon which the experiments were run
2.	System
    1.	How was the system obtained (easy – like a VM, or hard like a specific HW set-up)
    2.	How to configure the environment (e.g. environmental variables, paths et    3.)
    3.	How to compile the system (existing compilation options should be mentioned – what tools and which flags were used)
    4.	How to use the system (what config options/parameters were passed into the system)
    5.	How to validate the system was correctly installed (tests with expected output to validate the system has been set-up properly)
3.	Tools
    1.	Recommended to use ReproZip to capture environment, input, expected output and required libraries.
    2.	More tools available at [here](https://reproduciblescience.org/reproducibility-directory/)
4.	Experiments
    1.	For each set of results, expect the following steps:
        1.	Set-up phase where parameters are configured and data is loaded
        2.	Running phase where workload is applied and measurements taken
        3.	Clean-up phase where the state of the system is prepared to avoid interference for next round of experiments
    2.	For each set of experiments, provide the following for each phase;
        1.	How to perform the setup, running and clean-up phases (instructions / documented set-up scripts)
        2.	How to check that each phase ran as expected
        3.	Document the expected effect of the set-up phase (e.g. cold/warm cache status)
        4.	Document the expected effects in each step of the running phase
5.	Graphs and Plots
    1.	For each graph/plot
        1.	How is it obtained from experimental measurements
        2.	Which scripts / spreadsheets / tools were used to obtain the graphs – use of Gnuplot or matplotlib encouraged for plot generation
6.	Ideal submission
    1.	Complete set of scripts to install the system, produce the data, run the experiments and produce the resulting graphs along with a detailed readme file that describes the process step by step so it can be reproduced by the reviewer.
    2.	Should contain a master script that does the following:
        1.	Installs all the systems needed
        2.	Generated or fetches all the needed input data
        3.	Re-runs all experiments and generates all the results
        4.	Generates all the graphs, plots
        5.	Recompiles the sources of the paper
        6.	Generate a PDF for the paper that contains all the new graphs

## PVLDB definition

Much less well defined than SIGMOD - [PLVDB Repoducibility guidelines](http://vldb.org/pvldb/reproducibility/#submissions)

Summary of requirements is as follows:
1.	Title, abstract or accepted PVLDB paper
2.	Link to original paper
3.	Short description of how the reviewer can retrieve the reproducibility submission 
    1.	Link to code
    2.	How to use scripts for the following tasks:
        1.	Code  compilation
        2.	Data generation
        3.	Experimentation
4.	Short description of the HW needed to run code
    1.	Details specs on unusual or not commercially available HW
    2.	If specialised HW – include plans on how to give the reviewers access to this HW
5.	Short description of any software / data needed to run code and reproduce experiments
    1.	Particular attention should be given to restricted access items such as commercial SW that doesn’t have a free demo/academic version – include plans to allow reviewers access to any required SW or data
They also provide some context on the process the reviewers will use and so give some more information:
1.	Availability
    1.	System opacity
        1.	White box solution
            1.	Source
            2.	Config files
            3.	Build environment
        2.	Fully specified black box solution
    2.	Input data – either scripts to generate, actual data, or link to data
    3.	Experiment set
        1.	System config
        2.	Initialisation
        3.	Scripts
        4.	Workload
        5.	Measurement protocol
    4.	Scripts needed to transform raw data into graphs used in paper
2.	Replicability – the results generated should support the conclusions of the paper
3.	Reproducibility
    1.	Flexibility of the result sets
        1.	Ideally, test on multiple points along the following fronts:
            1.	Input data distributions
            2.	Workload characteristics
            3.	Diverse HW
        2.	If not available, then provide short description of other possible tests that could be done
            1.	Provide script parameters that can be used to stage and manage these different test conditions
    4.	Process – the review is carried out by particular DB groups, maybe tailor your scripts style to one that is familiar to those groups.


### PVLDB sample reproducibility submissions

1. Leveraging Similarity joins for Signal Reconstruction.
2. An Eight-Dimensional Systematic Evaluation of Optimized Search Algorithms on Modern Processors
3. GPU Rasterization for Real-Time Spatial Aggregation over Arbitrary Polygons
    1. Section 6 (implementation) and 7 (Experimental evaluation) covers most of what we need in reproducibility:
        1. Implemented on C++ and OpenGL.
        2. HW config
        3. Data sets – location from a reference plus operations used to convert
        4. Queries – single aggregate used as a representative query
        5. Establishing baselines – OpenMP used
        6. Configuration parameters for the GPU
        7. Cycling parameters to simulate user behaviour
        8. Evaluating unexpected scenario such as disk resident data on an expected in-memory system