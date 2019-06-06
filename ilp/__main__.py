import sys

from utils import Data, MethodType, write_result
from .ilp import ilp

data = Data.from_instance(sys.argv[1], sys.argv[2])

result = ilp(data)

write_result(result, MethodType.ILP, sys.argv[1], sys.argv[2])
