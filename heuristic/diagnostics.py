from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utils import State
from .operators import OPERATORS


def diagnostics(last: State,
                best: State,
                history: List[float],
                weights: List):
    """
    Outputs some diagnostics as a plot, and text to stdout.
    """
    print(f"Final result: {last.objective()}")
    print(f"Best observed: {best.objective()} (at"
          f" iteration {history.index(best.objective())})")

    # Plot of objective over time
    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(211)

    sns.lineplot(x=list(range(1, len(history) + 1)), y=history, ax=ax1)

    plt.title("Objective quality as a function of iterations")
    plt.ylabel("Objective value")
    plt.xlabel("Iteration (#)")

    # Plot of operator probabilities over time
    ax2 = fig.add_subplot(212)

    weights = pd.DataFrame(weights, columns=[operator.__name__
                                             for operator in OPERATORS])

    sns.lineplot(data=weights, ax=ax2)

    plt.title("Operator probabilities as a function of iterations")
    plt.ylabel("Pr[Operator]")
    plt.xlabel("Iteration (#)")

    plt.show()
