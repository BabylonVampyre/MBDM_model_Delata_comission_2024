# EPA Policy Analysis for IJssel River

As part of EPA141A, Model Based Decision Making, this code helps analyse which policy decisions
need to be made in order to minimize harm such as deaths and damages while keeping costs low under different scenarios. The policy analysis
is done based on [Alessio Ciullo's Dike Model](https://github.com/quaquel/epa141A_open).

Created by group 26, representing the Delta comisssion.
- Gabriella Low Chew Tung (5973058)
- Yashi Punia (6045979)
- Joppe Roosendaal (5087325)
- Emma Bokel (50110241)

The code is accompanied by a report analyzing the results. 

## Dependencies
To run this, make sure all these libraries are installed, this can also be done by using the requirements.txt file. 

- numpy~=1.26.4
  - ```pip install numpy```
- scipy~=1.13.0
  - ```pip install scipy```
- pandas~=2.2.2
  - ```pip install pandas```
- matplotlib~=3.9.0
  - ```pip install matplotlib```
- seaborn~=0.13.2
  - ```pip install seaborn```
- networkx~=3.3
  - ```pip install networkx```
- ema_workbench~=2.5.1
  - ```pip install ema_workbench```
- SALib~=1.5.0
  - ```pip install SALib```

## Repository Structure

### Files
The previous structure from Ciuollo's code was kept the same. Some files have been added or modified, which are listed here.

#### [problem formulation](problem_formulation.py)
 - This is the original problem formulation notebook given in the final assignment folder which has been adjusted.
#### [feature scoring](FeatureScoring.ipynb)
 - This file was used to generate the heatmaps for the final GSA that is in report appendix/
#### [Global Sensitivity Analysis Sobol](GSA_sobol%20-%20Copy.py)
 - This file was used to conduct and generate data for Sobol analysis using sobol uncertainty sampling.
#### [Sobal Analysis](Sobol Analysis.ipynb)
 - This file contains code that analyses Sobol results
#### [Dike Model Optimization for Directed Search](dike_model_optimization-for-directed-search.py)
 - This file was used to conduct MOEA and generate candidate policy solutions.
#### [Analysis of Directed Search](Analysis of Directed Search.ipynb)
 - This file calculates and evaluates convergence from directed search policy design
#### [Robustness Evaluation](Robustness_Evaluation.py)
 - This file was used for the generation of data when re-evaluating the selected policies under multiple scenarios. The data generated here is used in Robustness_evaluation.ipynb.
#### [Robustness Evaluation Notebook](Robustness_Evaluation.ipynb)
 - This file contians filtering of candidate policies and used to calculate and analyse robustness metrics for policies.

### Folders
The repository also contains the following folders
#### data
 - came with final assignment files
#### directed search results
 - contains all results from directed search method
#### robustness_final
 - contains plots and policies used in robustness evaluation
#### sobol_plots
 - contains plots from intial sobol analysis
#### results
 - contains data generated for initial sobol analysis



