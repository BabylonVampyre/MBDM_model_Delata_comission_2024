import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

from ema_workbench import (
    Model,
    Policy,
    ema_logging,
    SequentialEvaluator,
    MultiprocessingEvaluator,
)
from dike_model_function import DikeNetwork  # @UnresolvedImport
from problem_formulation import get_model_for_problem_formulation, sum_over, sum_over_time

import copy

#from multiprocessing import Process, freeze_support
if __name__ == '__main__':

    ema_logging.log_to_stderr(ema_logging.INFO)

    # choose problem formulation number, between 0-5
    # each problem formulation has its own list of outcomes
    dike_model, planning_steps = get_model_for_problem_formulation(5)

    # enlisting uncertainties, their types (RealParameter/IntegerParameter/CategoricalParameter), lower boundary, and upper boundary

    for unc in dike_model.uncertainties:
        print(repr(unc))

    uncertainties = copy.deepcopy(dike_model.uncertainties)

    # enlisting policy levers, their types (RealParameter/IntegerParameter), lower boundary, and upper boundary
    for policy in dike_model.levers:
        print(repr(policy))

    levers = copy.deepcopy(dike_model.levers)

    # enlisting outcomes
    for outcome in dike_model.outcomes:
        print(repr(outcome))

    outcomes = [i for i in dike_model.outcomes]

#freeze_support()
# running the model through EMA workbench
#with SequentialEvaluator(dike_model) as evaluator:
#    results = evaluator.perform_experiments(scenarios=10, policies=4)

# running the model through EMA workbench
#with SequentialEvaluator(dike_model) as evaluator:
#    results = evaluator.perform_experiments(scenarios=50, policies=4)

# running the model through EMA workbench
    with MultiprocessingEvaluator(dike_model) as evaluator:
        results = evaluator.perform_experiments(scenarios=50, policies=4)