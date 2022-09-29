class Expression:
    @staticmethod
    def is_number(number):
        return type(number) == int or type(number) == float

    @staticmethod
    def is_string(name):
        return type(name) == str

    @staticmethod
    def is_expression(my_object):
        if not isinstance(my_object, Expression):
            raise ValueError("Operands must be instances of class Expression!")

    @staticmethod
    def derivative(my_expression):
        Expression.is_expression(my_expression)
        return my_expression.sub_derivative()

    def __add__(self, second_operand):
        Expression.is_expression(second_operand)
        return Add(self, second_operand)

    def __mul__(self, second_operand):
        Expression.is_expression(second_operand)
        return Times(self, second_operand)


class Times(Expression):
    def __init__(self, x, y):
        Expression.is_expression(x)
        Expression.is_expression(y)
        self.first_operand = x
        self.second_operand = y

    def __str__(self):
        return str(self.first_operand) + "*" + str(self.second_operand)

    def evaluate(self, variables):
        return self.first_operand.evaluate(variables) * self.second_operand.evaluate(variables)

    @staticmethod
    def sub_derivative(self):
        return Add(Times(self.first_operand.derivative(),self.second_operand),
                   Times(self.first_operand,self.second_operand.derivative()))


class Add(Expression):
    def __init__(self, x, y):
        Expression.is_expression(x)
        Expression.is_expression(y)
        self.first_operand = x
        self.second_operand = y

    def __str__(self):
        return "(" + str(self.first_operand) + "+" + str(self.second_operand) + ")"

    def evaluate(self, variables):
        return self.first_operand.evaluate(variables) + self.second_operand.evaluate(variables)

    @staticmethod
    def sub_derivative(self):
        return Add(self.first_operand.derivative(),self.second_operand.derivative())

class Constant(Expression):
    def __init__(self, x):
        if Expression.is_number(x):
            self.val = x
        else:
            raise ValueError("Invalid input! Use integers or floats only.")

    def __str__(self):
        if self.val < 0:
            return "(" + str(self.val) + ")"
        else:
            return str(self.val)

    def evaluate(self, _):
        return self.val

    @staticmethod
    def sub_derivative(self):
        return Constant(0)


class Variable(Expression):
    def __init__(self, x):
        if Expression.is_string(x):
            self.name = x
        else:
            raise ValueError("Invalid input! Use strings only.")

    def __str__(self):
        return self.name

    def evaluate(self, variables):
        value = variables.get(self.name)
        if value is None:
            raise KeyError("No value for variable " + self.name)
        else:
            return value

    @staticmethod
    def sub_derivative(self):
        return Constant(1)


if __name__ == "__main__":
    expression = Times(Add(Variable("x"), Constant(2)), Variable("x"))
    print(str(expression))
    print(str(Expression.derivative(expression)))

    # print(expression.evaluate({"x": 2, "y": 3}))
    # print(str(expression + expression))
    # print((expression + expression).evaluate({"x": 2, "y": 3}))
