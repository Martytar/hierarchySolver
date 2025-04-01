import sympy as sp
import numpy as np

class TreeFunction:
    def __init__(self, variables, primaryNode=None):
        self.variables = variables
        self.primaryNode = primaryNode

    def calculate(self, values):
        return self.primaryNode.calculate(values, self.variables)

    class Node:
        def __init__(self, evaluation=None, links=None, expression=None):
            self.evaluation = evaluation
            self.links = links if links is not None else []
            self.expression = expression


        def calculate(self, values, variables):
            if self.expression is not None:
                res = self.expression
                for i in range(len(variables)):
                    for j in range(len(res)):
                        res[j] = res[j].subs(variables[i], values[i])

                return res
            elif self.links is not None:
                mini = 0
                minv = self.links[0].evaluation.subs(list(zip(variables, values)))
                for i in range(1, len(self.links)):
                    cv = self.links[i].evaluation.subs(list(zip(variables, values)))
                    if minv > cv:
                        mini = i
                        minv = cv
                return self.links[mini].calculate(values, variables)
            else:
                raise Exception("Incorrect structure of the TreeFunction")

