from ema_workbench import (
    Model,
    MultiprocessingEvaluator,
    SequentialEvaluator,
    ScalarOutcome,
    IntegerParameter,
    optimize,
    Scenario
)

from ema_workbench.em_framework.optimization import (ArchiveLogger,
                                                     EpsilonProgress)

from ema_workbench import Constraint
from ema_workbench.util import ema_logging

from problem_formulation import get_model_for_problem_formulation
import matplotlib.pyplot as plt
import seaborn as sns

from ema_workbench import Constraint



if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)

    model, steps = get_model_for_problem_formulation(2)

    reference_values = {
        "Bmax": 175,
        "Brate": 1.5,
        "pfail": 0.5,
        "discount rate 0": 1.5,
        "discount rate 1": 1.5,
        "discount rate 2": 1.5,
        "ID flood wave shape": 4,
        "num_events": 60
    }
    scen1 = {}

    for key in model.uncertainties:
        name_split = key.name.split("_")

        if (len(name_split) == 1) or key.name =='num_events':
            scen1.update({key.name: reference_values[key.name]})

        else:
            scen1.update({key.name: reference_values[name_split[1]]})

    ref_scenario = Scenario("reference", **scen1)

    constraints = [Constraint("Expected Number of Deaths", outcome_names="Expected Number of Deaths", function=lambda x : max(0,x-0.001)),
                   Constraint("Total Investment Costs", outcome_names="Total Investment Costs", function=lambda x: max(0,x-300e6))]

    #convergence_metrics = [EpsilonProgress()]

    espilon = [0.01] * len(model.outcomes)
    # Not sure if this is the correct epsilon value. May be too low.

    convergence_metrics = [ArchiveLogger(
        "directed search results",
        [l.name for l in model.levers],
        [o.name for o in model.outcomes],
        base_filename="directed_search_convergence_big_nfe.tar.gz",
    ),
        EpsilonProgress(),
    ]

    nfe = 20000 #10000


    with MultiprocessingEvaluator(model) as evaluator:
    #with SequentialEvaluator(model) as evaluator:
        results, convergence = evaluator.optimize(
            nfe=nfe,
            searchover="levers",
            epsilons=espilon,
            convergence=convergence_metrics,
            reference=ref_scenario,
            constraints=constraints
            )
    #
    results.to_csv("directed search results/dike_model_policy_design_big_nfe.csv")
    convergence.to_csv("directed search results/dike_model_policy_design_convergence_big_nfe.csv")

