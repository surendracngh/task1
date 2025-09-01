import numpy as np
from scipy import stats

arr = np.array([1, 2, 2, 3, 3, 3, 4, 5])

mode_result = stats.mode(arr)
print("Mode:", mode_result.mode[0])
print("Count:", mode_result.count[0])
