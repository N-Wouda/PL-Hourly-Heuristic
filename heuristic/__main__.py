import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import simplejson as json

from .Data import Data
from .adaptive_large_neighbourhood_search import \
    adaptive_large_neighbourhood_search
from .operators import OPERATORS

with open(f"experiments/{sys.argv[1]}/{sys.argv[2]}.json") as file:
    data = Data(json.load(file))

# Fixes a seed (useful for testing)
np.random.seed(19680801)

result, best, history, weights = adaptive_large_neighbourhood_search(data)

# Objective values
print("Final result:", result.evaluate())
print("Best observed:", best.evaluate())

# Plot of objective over time, and operator weights
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)

sns.lineplot(x=list(range(1, len(history) + 1)), y=history, ax=ax1)

plt.title("Objective quality as a function of iterations")
plt.ylabel("Objective value")
plt.xlabel("Iteration (#)")

ax2 = fig.add_subplot(212)

weights = pd.DataFrame(weights, columns=[operator.__name__
                                         for operator in OPERATORS])

sns.lineplot(data=weights, ax=ax2)

plt.title("Operator probabilities as a function of iterations")
plt.ylabel("Pr[Operator]")
plt.xlabel("Iteration (#)")

plt.show()
