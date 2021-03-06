from knapsack.core import *
from random import random as rnd
from numpy import random as np_rnd
import statistics as stat

def rand_problem_dense(N: int):
    weights = [int(rnd() * N) for I in range(N)]
    profits = [rnd() for I in range(N)]
    MaxWeights = int(0.5 * (sum(weights)))
    return profits, weights, MaxWeights


def rand_problem_sparse(N: int):
    weights = [int(rnd() * N) + N for I in range(N)]
    profits = [rnd() for I in range(N)]
    MaxWeights = int(2 * stat.median(weights))
    return profits, weights, MaxWeights


def rand_problem_exponential(scale: int, itemsCount: int, satruration):
    assert 0 < satruration < 1
    Profits, Weights = np_rnd.exponential(scale=scale, size=(2, itemsCount))
    Profits, Weights = map(lambda x: int(x), Profits), map(lambda x:int(x), Weights)
    Profits, Weights = list(Profits), list(Weights)
    Budget = int(satruration*sum(W for W in Weights))
    return Profits, Weights, Budget



def main():
    def bb_vs_dp(N:int, n:int):
        Saturation = 0.3
        ProblemList = [rand_problem_dense(n) for I in range(N)] + [rand_problem_sparse(n) for I in range(N)]
        ProblemList += [rand_problem_exponential(n, 0.3) for I in range(N)]
        for P, W, B in ProblemList:
            S1, Opt1 = branch_and_bound(P, W, B)
            S1.sort()
            print(f"bb: {S1}")
            S2, Opt2 = knapsack_dp_primal(P, W, B)
            S2.sort()
            print(f"dp: {S2}")
            assert str(S1) == str(S2), f"{S1}={sum(P[I] for I in S1)}, {S2}={sum(P[I] for I in S2)}" + \
                f"Details: P = {P}\n  W={W}\n B={B}"

    bb_vs_dp(100, 4)
    bb_vs_dp(100, 20)
    bb_vs_dp(10, 100)
    bb_vs_dp(5, 200)

    pass

if __name__ == "__main__":
    main()