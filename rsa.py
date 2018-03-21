import numpy as np
import matplotlib.pyplot as plt
#from math import exp
import math


class Model:
    def __init__(self):
        self.sPrior = {90: 0.1, 80: 0.3, 70: 0.35, 60: 0.1, 50: 0.15}
        self.aPrior = {90: 0.00625, 80: 0.35, 70: 0.5, 60: 0.9, 50: 0.975}

        self.sList = [90, 80, 70, 60, 50]
        self.uList = [90, 80, 70, 60, 50, 50]
        self.cList = [1, 1, 1, 1, 1, 0.5]
        self.aList = [1, 0]
        # self.sPrior = sPrior

        # self.aPrior = aPrior
        self.gList = [self.gs, self.ga, self.gsa] #list of functions
        result = self.L1List(50, 1)
        print(result)
        #result = self.L1List(50, 1)
        #print(result)
        plt.bar(list(range(1, 6))+list(range(1, 6)), height = result)
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

    def S1(self, u, s, a, g, cost):
        num = 0.0
        for sx in self.sList:
            for ax in self.aList:
                if g(sx, ax) == g(s, a):
                    num += self.L0(sx, ax, u) * pow(math.e, -cost)
        return num

    def S1norm(self, u, s, a, g, cost):
        denom = 0.0
        for i in range(len(self.uList)):
            #print ux, s, a, self.S1(ux, s, a, g)
            ux = self.uList[i]
            cx = self.cList[i]
            denom += self.S1(ux, s, a, g, cx)
            # if(ux==50):
            #     print(ux, cx)
            #     print(self.S1(ux, s, a, g, cx))
        if denom == 0: return 0
        num = self.S1(u, s, a, g, cost)
        if num != 0: print(u, s, a, num, denom)
        return num/denom

    def L1(self, s, a, u, cost):
        num = 0.0
        for g in self.gList:
            #print self.Ps(s), self.Pa(a, s), self.Pg(g), self.S1(u, s, a, g)
            num += self.Ps(s) * self.Pa(a, s) * self.Pg(g) * self.S1norm(u, s, a, g, cost)
        #if num!= 0: print(num)
        return num

    def L1List(self, u, cost):
        denom = 0.0
        list = []
        for si in range(len(self.sList)):
            s = self.sList[si]
            for a in self.aList:
                denom += self.L1(s, a, u, cost)

        for a in self.aList:
            for si in range(len(self.sList)):
                s = self.sList[si]
                num = self.L1(s, a, u, cost)
                #print(num, denom)
                list.append(num/denom)
        return list

A = Model()

