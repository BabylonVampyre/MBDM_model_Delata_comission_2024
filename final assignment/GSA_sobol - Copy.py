import numpy as np
import scipy as sp
import pandas as pd
import networkx as nx
import copy
import mpi4py


from ema_workbench import (
    Model,
    Policy,
    RealParameter,
    ScalarOutcome,
    ema_logging,
    perform_experiments,
    MPIEvaluator,
    MultiprocessingEvaluator,
    save_results,
)


from SALib.analyze import sobol
from ema_workbench import Samplers
from ema_workbench.em_framework.salib_samplers import get_SALib_problem

    
from dike_model_function import DikeNetwork  # @UnresolvedImport
from problem_formulation import get_model_for_problem_formulation, sum_over, sum_over_time

def analyze(results, kpi):
    """analyze results using SALib sobol, returns a dataframe"""
    _, outcomes = results
    
    problem = get_SALib_problem(dike_model.uncertainties)
    y = outcomes[kpi]
    sobol_indices = sobol.analyze(problem, y, calc_second_order=True, print_to_console=False)
    sobol_stats = {key: sobol_indices[key] for key in ["ST", "ST_conf", "S1", "S1_conf"]}
    sobol_stats = pd.DataFrame(sobol_stats, index=problem["names"])
    sobol_stats.sort_values(by="ST", ascending=False)
    s2 = pd.DataFrame(sobol_indices["S2"], index=problem["names"], columns=problem["names"])
    s2_conf = pd.DataFrame(sobol_indices["S2_conf"], index=problem["names"], columns=problem["names"])
    return sobol_stats, s2, s2_conf


if __name__ == "__main__":
# We recommend setting pass_root_logger_level=True when running on a cluster, to ensure consistent log levels.
    ema_logging.log_to_stderr(level=ema_logging.INFO, pass_root_logger_level=True)

    #----------------------------------------------------------------------------------------------
    # choose problem formulation number, between 0-5
    # each problem formulation has its own list of outcomes
    dike_model, planning_steps = get_model_for_problem_formulation(5)
    
    # enlisting uncertainties, their types (RealParameter/IntegerParameter/CategoricalParameter), lower boundary, and upper boundary
    uncertainties = copy.deepcopy(dike_model.uncertainties)
    
    # enlisting policy levers, their types (RealParameter/IntegerParameter), lower boundary, and upper boundary
    levers = copy.deepcopy(dike_model.levers)

    # defining specific policies
    # for example, policy 1 is about extra protection in upper boundary
    # policy 2 is about extra protection in lower boundary
    # policy 3 is extra protection in random locations


    #def get_do_nothing_dict():
    #    return {l.name: 0 for l in dike_model.levers}

    #do_nothing = Policy(
     #       "policy 0",
     #       **dict(
     #           get_do_nothing_dict()
     #       )
     #   )

    #policies = [
    #    Policy(
    #        "policy 1",
    #        **dict(
    #            get_do_nothing_dict(),
    #            **{"0_RfR 0": 1, "0_RfR 1": 1, "0_RfR 2": 1, "A.1_DikeIncrease 0": 5}
    #        )
    #    ),
    #    Policy(
    #        "policy 2",
    #        **dict(
    #            get_do_nothing_dict(),
    #            **{"4_RfR 0": 1, "4_RfR 1": 1, "4_RfR 2": 1, "A.5_DikeIncrease 0": 5}
    #        )
    #    ),
    #    Policy(
    #        "policy 3",
    #        **dict(
    #            get_do_nothing_dict(),
    #            **{"1_RfR 0": 1, "2_RfR 1": 1, "3_RfR 2": 1, "A.3_DikeIncrease 0": 5}
    #        )
    #   ),
    #]

    test=pd.read_csv("Filtered Policies - to be tested for robustness.csv",index_col=0)
    test=test.drop(labels=['RfR_agg'],axis=1)
    policies=test.to_dict('index')
    policies=[Policy(f"policy {k}", **dict(v)) for k,v in policies.items()]




    
#------------------------------------------------------------------------------------------------------------
    # Note that we switch to the MPIEvaluator here
    n_scenarios = 1000
    #n_policies = 1
    with MultiprocessingEvaluator(dike_model) as evaluator:
    #with MPIEvaluator(dike_model) as evaluator:
            results=evaluator.perform_experiments(scenarios=n_scenarios, policies=policies,uncertainty_sampling=Samplers.SOBOL) #
 
    # Save the results
    save_results(results, "directed search results/dike_model_test_sobol_uncertainty_sampling_on_resultant_policies.tar.gz")

    experiments, outcomes = results
    
    kpi_list=list(outcomes.keys())

    for ooi in kpi_list:
        sobol_stats, s2, s2_conf = analyze(results, ooi)
        save_results(sobol_stats, f"results/sobol_stats_{ooi}.tar.gz")
        save_results(s2, f"results/s2_{ooi}.tar.gz")
        save_results(s2_conf, f"results/s2_conf_{ooi}.tar.gz")

    




    
