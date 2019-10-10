from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import numpy as np

ResultItem = Union[int, float, str]
Num = Union[int, float]

Result = List[Dict[str, ResultItem]]

PowerDivergenceItem = Union[float, np.ndarray]
PowerDivergence = Tuple[PowerDivergenceItem, PowerDivergenceItem]

ChiSquareItem = Union[float, np.ndarray]
ChiSquare = Tuple[ChiSquareItem, ChiSquareItem]
