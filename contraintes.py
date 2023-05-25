from pprint import pprint
from time import sleep
from typing import List, Tuple
import subprocess
from itertools import combinations
Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]


def exactly_k(k: int, variables: List[PropositionnalVariable]) -> ClauseBase:
    r: ClauseBase = []
    for tab in combinations(variables, k+1):
        r.append([-x for x in tab])
    for tab in combinations(variables, len(variables)+1-k):
        r.append([x for x in tab])
    return r



#retourne l'ensemble de clause traitant la contrainte : "au moins n variables vraies dans la liste"
def at_least_k(k: int, variables: List[PropositionnalVariable]) -> ClauseBase:
    r: ClauseBase = []
    for tab in combinations(variables, len(variables)+1-k):
        r.append([x for x in tab])
    return r