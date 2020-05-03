from alns.criteria import SimulatedAnnealing

# 12 * 48 = 576 regular modules, so the final index/ID for self-study is 576.
SELF_STUDY_MODULE_ID = 576

WEIGHTS = [25, 10, 1, 0.5]
ITERATIONS = 10000
CRITERION = SimulatedAnnealing(1000, 1, step=0.9995, method="exponential")
DECAY = 0.8
DEGREE_OF_DESTRUCTION = 0.2
