import sympy as sp
import numpy as np


class TreeFunction:
    def __init__(self, variables, primaryNode=None):
        self.input_dimension = len(variables)
        self.output_dimension = None
        self.variables = variables
        self.primaryNode = primaryNode
        if primaryNode is not None:
            if primaryNode.related_tree_function is None:
                primaryNode.related_tree_function = self

    def calculate(self, values):
        return self.primaryNode.calculate(values, self.variables)

    class Node:
        def __init__(self, evaluation=None, links=None, expression=None, related_tree_function=None):
            self.evaluation = evaluation
            self.related_tree_function = related_tree_function
            self.links = links if links is not None else []
            self.expression = expression

        def calculate(self, values, variables):
            if self.expression is not None:
                res = self.expression
                for i in range(len(variables)):
                    for j in range(len(res)):
                        res[j] = res[j].subs(variables[i], values[i])

                return np.array(res).reshape(-1)
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


class LinearCombinationFunction:
    def __init__(self, coefficients, functions):

        input_dimension = 0
        output_dimension = 0
        for f in functions:
            input_dimension += f.input_dimension
            output_dimension += f.output_dimension
        self.input_dimension = input_dimension
        self.output_dimension = output_dimension

        if len(coefficients) < output_dimension:
            raise ValueError(f"Not enough coefficients. Dimension is {output_dimension}")
        if len(coefficients) > output_dimension:
            raise ValueError(f"Too many coefficients. Dimension is {output_dimension}")
        self.coefficients = coefficients
        self.functions = functions



    def calculate(self, values):
        if self.input_dimension > len(values):
            raise ValueError(f"Not enough values to calculate function Function dimension is {self.input_dimension}")
        if self.input_dimension < len(values):
            raise ValueError(f"Too many values. Function dimension is {self.input_dimension}")

        value_index = 0
        coef_index = 0
        result = 0
        for i in range(len(self.functions)):
            cf = self.functions[i]
            cc = self.coefficients[coef_index:(coef_index + cf.output_dimension)]
            result += np.matmul(cc, cf.calculate(values[value_index:(value_index + cf.input_dimension)]))

            value_index == cf.input_dimension
            coef_index += cf.output_dimension
        return result
