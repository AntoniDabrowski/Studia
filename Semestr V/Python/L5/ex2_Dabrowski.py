from itertools import combinations


class Formula:
    @staticmethod
    def is_expression(my_object):
        if not isinstance(my_object, Formula):
            raise ValueError("Operands must be instances of class Formula!")

    @staticmethod
    def tautology(first_expression, second_expression):
        # I am familiar with different approaches to SAT problem, which is equivalent to this one,
        # but optimization is not the point of this task, so I simply check all the possibilities.
        Formula.is_expression(first_expression)
        Formula.is_expression(second_expression)
        variables_1 = first_expression.get_variables()
        variables_2 = second_expression.get_variables()

        if not variables_1 and variables_2:
            val_one = first_expression.evaluate({})
            for i in range(len(variables_2) + 1):
                for j, combination in enumerate(combinations(variables_2, i)):
                    valuation = {key: (True if key in combination else False) for key in variables_2}
                    value = second_expression.evaluate(valuation)
                    if val_one != value:
                        return False
            return True

        elif variables_1 and not variables_2:
            val_second = second_expression.evaluate({})
            for i in range(len(variables_1) + 1):
                for j, combination in enumerate(combinations(variables_1, i)):
                    valuation = {key: (True if key in combination else False) for key in variables_1}
                    value = first_expression.evaluate(valuation)
                    if val_second != value:
                        return False
            return True

        elif not variables_1 and not variables_2:
            return first_expression.evaluate({}) == second_expression.evaluate({})

        elif variables_1 == variables_2:
            for i in range(len(variables_1) + 1):
                for combination in combinations(variables_1, i):
                    valuation = {key: (True if key in combination else False) for key in variables_1}
                    if first_expression.evaluate(valuation) != second_expression.evaluate(valuation):
                        return False
            return True
        else:
            for i in range(len(variables_1) + 1):
                for j, combination in enumerate(combinations(variables_1, i)):
                    valuation = {key: (True if key in combination else False) for key in variables_1}
                    current_value = first_expression.evaluate(valuation)
                    if i == 0 and j == 0:
                        previous_value = current_value
                    if previous_value != current_value:
                        return False
                    previous_value = current_value
            for i in range(len(variables_2) + 1):
                for j, combination in enumerate(combinations(variables_2, i)):
                    valuation = {key: (True if key in combination else False) for key in variables_2}
                    if second_expression.evaluate(valuation) != previous_value:
                        return False
            return True

    def __add__(self, second_operand):
        Formula.is_expression(second_operand)
        return And(self, second_operand)

    def __mul__(self, second_operand):
        Formula.is_expression(second_operand)
        return Or(self, second_operand)

    def simplify(self):
        return self


class Or(Formula):
    def __init__(self, x, y):
        Formula.is_expression(x)
        Formula.is_expression(y)
        self.first_operand = x
        self.second_operand = y

    def __str__(self):
        return "(" + str(self.first_operand) + "∨" + str(self.second_operand) + ")"

    def evaluate(self, variables):
        return self.first_operand.evaluate(variables) | self.second_operand.evaluate(variables)

    def get_variables(self):
        return self.first_operand.get_variables() | self.second_operand.get_variables()

    def simplify(self):
        left = self.first_operand.simplify()
        right = self.second_operand.simplify()
        if left == Constant(False) and right == Constant(False):
            return Constant(False)
        elif left == Constant(False):
            return right
        elif right == Constant(False):
            return left
        else:
            return self


class And(Formula):
    def __init__(self, x, y):
        Formula.is_expression(x)
        Formula.is_expression(y)
        self.first_operand = x
        self.second_operand = y

    def __str__(self):
        return "(" + str(self.first_operand) + "∧" + str(self.second_operand) + ")"

    def evaluate(self, variables):
        return self.first_operand.evaluate(variables) & self.second_operand.evaluate(variables)

    def get_variables(self):
        return self.first_operand.get_variables() | self.second_operand.get_variables()

    def simplify(self):
        left = self.first_operand.simplify()
        right = self.second_operand.simplify()
        if left == Constant(False) or right == Constant(False):
            return Constant(False)
        else:
            return self


class Not(Formula):
    def __init__(self, operand):
        self.operand = operand

    def __str__(self):
        return "¬" + str(self.operand)

    def evaluate(self, variables):
        return not self.operand.evaluate(variables)

    def get_variables(self):
        return self.operand.get_variables()


class Constant(Formula):
    def __init__(self, val):
        if type(val) == bool:
            self.val = val
        else:
            raise ValueError("Invalid input! Use integers or floats only.")

    def __str__(self):
        return str(self.val)

    def __eq__(self, second_operand):
        if isinstance(second_operand, Constant) and self.val == second_operand.val:
            return True
        return False

    def evaluate(self, _):
        return self.val

    @staticmethod
    def get_variables():
        return set()


class Variable(Formula):
    def __init__(self, x):
        if type(x) == str:
            self.name = x
        else:
            raise ValueError("Invalid input! Use strings only.")

    def __str__(self):
        return self.name

    def evaluate(self, variables):
        value = variables.get(self.name)
        if value is None:
            raise KeyError("No value assigned to a variable " + self.name)
        else:
            return value

    def get_variables(self):
        return {self.name}


if __name__ == "__main__":
    # I think that all my classes and methods matches the one described in homework so
    # I will not write detailed specification. One thing that was not clarified is the input
    # for evaluation method. I use dicts where keys are variables names and values are
    # booleans corresponding to them.

    # Testing formula from exercise list
    formula = Or(Not(Variable("x")), And(Variable("y"), Constant(True)))
    print(str(formula))                                         # (¬x∨(y∧True))
    print(formula.evaluate({"x": False, "y": False}))           # True
    print(formula.evaluate({"x": True, "y": False}))            # False
    print(Formula.tautology(formula, formula))                  # True
    print(Formula.tautology(formula, Constant(True)))           # False
    print(formula + Constant(True), "\n")                       # ((¬x∨(y∧True))∧True)

    # Interesting example
    formula_1 = Or(Variable("a"), Not(Variable("a")))
    formula_2 = Not(And(Variable("b"), Not(Variable("b"))))
    print(formula_1)                                            # (a∨¬a)
    print(formula_2)                                            # ¬(b∧¬b)
    print(Formula.tautology(formula_1, formula_2), "\n")        # True

    # Some border cases
    print(Formula.tautology(Constant(True), Constant(False)))   # False
    print(Formula.tautology(Constant(True), Constant(True)))    # True
    print(Formula.tautology(Constant(True), Variable("a")))     # False
    print(Formula.tautology(Variable("a"), Constant(True)))     # False
    print(Formula.tautology(Variable("a"), Variable("a")),"\n") # True


    # Testing simplify method
    formula_3 = And(Variable("p"), Constant(False))
    formula_4 = Or(Variable("p"), Constant(False))
    formula_5 = formula_3 + formula_4
    formula_6 = formula_3 * formula_4
    print(formula_3, " -> ", formula_3.simplify())              # (p∧False)  ->  False
    print(formula_4, " -> ", formula_4.simplify())              # (p∨False)  ->  p
    print(formula_5, " -> ", formula_5.simplify())              # ((p∧False)∧(p∨False))  ->  False
    print(formula_6, " -> ", formula_6.simplify())              # ((p∧False)∨(p∨False))  ->  p
