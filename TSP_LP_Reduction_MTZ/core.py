#   Miller Tucker Zemlin's Linear Programming Reduction of the Traveling Salesman Problem.
import math as math
import random as rnd
from graph.simple_digraph import *
from typing import *
from pulp import *
import matplotlib.pyplot as pyplt


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other.x != self.x:
            return False
        return other.y == self.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return super().__hash__()


class FullGraph2D(SimpleDiGraph):

    def __iadd__(self, p: Type[Point]):
        n = self.size()
        super().__iadd__(p)
        for I in range(n):
            V = self[I]
            self.connect_by_idx(I, n, dis(self._V[I], self._V[n]))
            self.connect_by_idx(n, I, dis(self._V[I], self._V[n]))
        return self


class TravelingSalesManLP(FullGraph2D):
    """
        This reduction has a polynomial number of constraints applied to the system, and it's formulated by
        Miller Tucker Zemlin.
        Here are the variable:
            x_{i, j}: Going from city i to city j at some point during the tour.
                * Binary
                * Direction counts.
            u_i: The step city i has been visited.
                2 <= i <= n
                u_i = t, then it means that city i is visted at t step of the tour.
                0 <= u_i <= n - 1

    """

    def formulate_lp(self):
        if not self.__changes:
            return
        self.__changes == False # The formulation will address the changes.
        n = self.size()
        self.P = LpProblem(sense=LpMinimize)
        self.u = LpVariable.dict("u", range(1, n), cat=LpInteger, lowBound=0, upBound=n - 1)
        EdgeIndexList = [(I, J) for I in range(n) for J in range(n) if I != J]
        FirstIndexList, SecondIndexList = [], []
        for I, J in EdgeIndexList:
            FirstIndexList.append(I); SecondIndexList.append(J)
        self.x = LpVariable.dict("x", (FirstIndexList, SecondIndexList), cat=LpBinary)
        # number of Incoming edges in path is exactly 1.
        for J in range(n):
            self.P += lpSum([self.x[I, J] for I in range(n) if I != J]) == 1
        # Outcoming edges in path is exactly 1
        for I in range(n):
            self.P += lpSum([self.x[I, J] for J in range(n) if J != I]) == 1
        # Excluding one vertex, the path must be simple!
        for I in range(1, n):
            for J in [J for J in range(1, n) if J != I]:
                self.P += lpSum(self.u[I] - self.u[J] + n*self.x[I, J]) <= n - 1
        # setting Object function:
        self.P += lpSum([self.c(I,J)*self.x[I, J] for I, J in EdgeIndexList])

    def c(self, I, J):
        V1 = self[I]
        V2 = self[J]
        return dis(V1, V2)

    def solve_path(self):
        self.formulate_lp()
        status = self.P.solve(PULP_CBC_CMD(msg=True, fracGap=0.05, maxSeconds=300))
        assert status == 1, f"LP status not good: {LpStatus[status]}"
        # Interpret solution, which is a path.
        Path = [0] # all vertex must be in the solution
        n = self.size()
        while len(Path) != n:
            for J in range(n):
                I = Path[-1]
                if self.x[I, J].varValue == 1:
                    Path.append(J)
                    break # optional.
        return Path

    def plot_path(self):
        pyplt.clf()
        Path = self.solve_path()
        for V1, V2 in zip(Path[:-1], Path[1:]):
            pyplt.scatter(self[V1].x, self[V1].y)
            pyplt.scatter(self[V2].x, self[V2].y)
            pyplt.plot([self[V1].x, self[V2].x], [self[V1].y, self[V2].y])
        V_n, V0 = Path[0], Path[-1]
        pyplt.plot([self[V_n].x, self[V0].x], [self[V_n].y, self[V0].y], '--')
        pyplt.show()

    def __init__(self):
        self.__changes = False # True means that the problem has been changed.
        super().__init__()


    def __iadd__(self, other):
        self.__changes = True
        return super().__iadd__(other)


def rand_points(topLeft, bottomRight, n):
    """

    :param topLeft:
    :param bottomRight:
    :param n:
    :return:
    """
    assert topLeft[0] < bottomRight[0] and topLeft[1] > bottomRight[1]
    def randPointInSquare():
        x = rnd.random()*(bottomRight[0] - topLeft[0]) + topLeft[0]
        y = rnd.random()*(topLeft[1] - bottomRight[1]) + bottomRight[1]
        return  Point(x, y)
    return [randPointInSquare() for I in range(n)]

def dis(a, b):
    """
        Euclidean distance between 2 points.
    :param a:
    :param b:
    :return:
    """
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def main():
    RandPoints = rand_points([0, 10], [10, 0], 30)
    FullG = TravelingSalesManLP()
    for P in RandPoints:
        FullG += P
    print(FullG)
    print(FullG.solve_path())
    FullG.plot_path()


    pass

if __name__ == "__main__":
    main()