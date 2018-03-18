import numpy as np
import matplotlib.pyplot as plt
#from math import exp
import math


class Model:
    def __init__(self):
        self.sPrior = {90: 0.6, 80: 0.25, 70: 0.1, 60: 0.04, 50: 0.01}
        self.aPrior = {90: 0.2, 80: 0.6, 70: 0.9, 60: 0.99, 50: 1}

        self.sList = [90, 80, 70, 60, 50]
        self.uList = [90, 80, 70, 60, 50]
        self.aList = [1, 0]
        # self.sPrior = sPrior

        # self.aPrior = aPrior
        self.gList = [self.gs, self.ga, self.gsa] #list of functions
        result = self.L1List(60)
        print(result)
        plt.bar(list(range(1, 6))+list(range(1, 6)),height = result)
        plt.show()


    def gs(self, s, a):
        return (s, -1)

    def ga(self, s, a):
        return (-1, a)

    def gsa(self, s, a):
        return (s, a)

    def Pa(self, a, s):
        if (a == 1): return self.aPrior[s]
        else: return 1-self.aPrior[s]

    def Ps(self, s):
        return self.sPrior[s]

    def Pg(self, g):
        return 1/float(len(self.gList))

    def L0(self, s, a, u):
        if (s==u): return self.Pa(a, s)
        else: return 0

    def S1(self, u, s, a, g):
        num = 0.0
        for sx in self.sList:
            for ax in self.aList:
                if g(sx, ax) == g(s, a):
                    num += self.L0(sx, ax, u) * pow(math.e, -1)
        return num

    def S1norm(self, u, s, a, g):
        denom = 0.0
        for ux in self.uList:
            #print ux, s, a, self.S1(ux, s, a, g)
            denom += self.S1(ux, s, a, g)
        if denom == 0: return 0
        return self.S1(u, s, a, g)/denom

    def L1(self, s, a, u):
        num = 0.0
        for g in self.gList:
            #print self.Ps(s), self.Pa(a, s), self.Pg(g), self.S1(u, s, a, g)
            num += self.Ps(s) * self.Pa(a, s) * self.Pg(g) * self.S1norm(u, s, a, g)
        return num

    def L1List(self, u):
        denom = 0.0
        list = []
        for s in self.sList:
            for a in self.aList:
                denom +=self.L1(s, a, u)

        for a in self.aList:
            for s in self.sList:
                list.append(self.L1(s, a, u)/denom)
        return list

A = Model()

