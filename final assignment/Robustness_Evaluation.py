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
    

if __name__ == "__main__":
    
    ema_logging.log_to_stderr(ema_logging.INFO)
    
    model, steps = get_model_for_problem_formulation(2)
    
    results_v0 = pd.read_csv("directed search results/dike_model_policy_design.csv",index_col=0)
    results_v1 = pd.read_csv("directed search results/dike_model_policy_design_big_nfe.csv",index_col=0)

    logical_1 = results_v0['Expected Number of Deaths']<0.001
    results_v0['RfR_agg']=results_v0.iloc[:,0:15].agg(['sum'],axis="columns")
    logical_2 = results_v0['RfR_agg']>=1
    logical_3 = results_v0['Expected Annual Damage']<0.01
    
    logical_11 = results_v1['Expected Number of Deaths']<0.001
    results_v1['RfR_agg']=results_v1.iloc[:,0:15].agg(['sum'],axis="columns")
    logical_21 = results_v1['RfR_agg']>=1
    logical_31 = results_v1['Expected Annual Damage']<0.01
    
    policies = pd.concat([results_v0[logical_1 & logical_2 & logical_3],results_v1[logical_11 & logical_21 & logical_31]])
    policies = policies.drop([o.name for o in model.outcomes], axis=1)
    policies = policies.drop(columns=['RfR_agg'])
    
    policies_to_evaluate = []
    for i, policy in policies.iterrows():
        policies_to_evaluate.append(Policy(str(i), **policy.to_dict()))

    
    n_scenarios = 1000
    
    print(f"Evaluating {len(policies_to_evaluate)} policies across {n_scenarios} scenarios")
    
    with MultiprocessingEvaluator(model) as evaluator:
        scenario_results = evaluator.perform_experiments(n_scenarios,policies_to_evaluate)
    
    save_results(scenario_results, "directed search results/policy_robustness_1000_scenarios.tar.gz")

