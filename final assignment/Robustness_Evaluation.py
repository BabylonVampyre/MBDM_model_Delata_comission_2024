from ema_workbench import (
    Model,
    MultiprocessingEvaluator,
    ScalarOutcome,
    IntegerParameter,
    optimize,
    Scenario,
    Policy,
    save_results
)
from ema_workbench.util import ema_logging

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import copy
from dike_model_function import DikeNetwork  # @UnresolvedImport
from problem_formulation import get_model_for_problem_formulation, sum_over, sum_over_time
import random
    

if __name__ == "__main__":

    random.seed(123)
    ema_logging.log_to_stderr(ema_logging.INFO)

    
    model, steps = get_model_for_problem_formulation(2)
    
    #results_v0 = pd.read_csv("directed search results/dike_model_policy_design.csv",index_col=0)
    results_v0 = pd.read_csv("directed search results/seed results/dike_model_policy_design_big_nfe.csv",index_col=0)

    #Double RfR filter
    projects = set()
    for col in results_v0.columns:
        if '_RfR' in col:
    
            projects.add(col.split('_')[0])
    # Initialize a boolean mask with False indicating rows to keep
    rows_to_delete = pd.Series([False] * len(results_v0))
    
    # Iterate over each project and update the mask
    for project in projects:
    
        # Get columns for the current project
        project_cols = [col for col in results_v0.columns if col.startswith(project)]
        # Update the mask for rows where the sum across the project's columns is greater than 1
        rows_to_delete |= results_v0[project_cols].sum(axis=1) > 1
    
    # Remove these rows from the DataFrame
    df_cleaned = results_v0[~rows_to_delete]
    results_v0 = df_cleaned


    logical_1 = results_v0['Expected Number of Deaths']<0.001
    results_v0['RfR_agg']=results_v0.iloc[:,0:15].agg(['sum'],axis="columns")
    logical_2 = results_v0['RfR_agg']>=0
    logical_3 = results_v0['Expected Annual Damage']<0.01

    

    # Filtering policies
    policies = results_v0[logical_1 & logical_2 & logical_3]
    policies.to_csv("robustness_final/Filtered Policies - to be tested for robustness.csv")
    policies = policies.drop([o.name for o in model.outcomes], axis=1)
    policies = policies.drop(columns=['RfR_agg'])
    
    policies_to_evaluate = []
    for i, policy in policies.iterrows():
        policies_to_evaluate.append(Policy(str(i), **policy.to_dict()))

    
    n_scenarios = 1000
    
    print(f"Evaluating {len(policies_to_evaluate)} policies across {n_scenarios} scenarios")
    
    with MultiprocessingEvaluator(model) as evaluator:
        scenario_results = evaluator.perform_experiments(n_scenarios,policies_to_evaluate)
    
    save_results(scenario_results, f"robustness_final/policy_robustness_{n_scenarios}_scenarios_final.tar.gz")

