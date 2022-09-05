import numpy as np


class Leaf:
    def __init__(self,v_name):
        self.name = v_name
        self.parent = None

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level+=1
            p = p.parent
        return level

    def print_tree(self):
        spaces = ' ' * (self.get_level()-1) * 3 if self.parent else ''
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + self.name)

class Node:
    def __init__(self, v_operator):
        self.operator = v_operator
        self.children = []
        self.parent = None

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level+=1
            p = p.parent
        return level

    def print_tree(self):
        spaces = ' ' * (self.get_level() - 1) * 3 if self.parent else ''
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + self.operator)
        if self.children:
            for child in self.children:
                child.print_tree()

def merge_nodes(left_node,right_node,operator):
    node = Node(operator)
    node.children.append(left_node)
    node.children.append(right_node)
    left_node.parent = node
    right_node.parent = node
    return node

def negation(current_node):
    node = Node("¬")
    node.children.append(current_node)
    current_node.parent = node
    return node

def execute(values,head):
    if isinstance(head,Leaf):
        try:
            return values[head.name]
        except:
            print("ERROR! There is no value assigned to variable", head.name)
    if isinstance(head,Node):
        if head.operator == '¬':
            return not execute(values,head.children[0])
        elif head.operator == '∧':
            return execute(values,head.children[0]) and execute(values,head.children[1])
        elif head.operator == '∨':
            return execute(values,head.children[0]) or execute(values,head.children[1])
        else:
            print("ERROR! Unknown operator -> ",head.operator)
    else:
        print("ERROR! Unknown object ", type(head))


def rec_import_formula(line):
    # assumption: there are all needed brackets
    if len(line) == 1:
        return Leaf(line)
    elif line[0] == '¬':
        return negation(rec_import_formula(line[2:-1]))
    else:
        bracket_counter = 1
        for i, element in enumerate(line[1:]):
            if bracket_counter==0:
                return merge_nodes(rec_import_formula(line[1:i]),rec_import_formula(line[i+3:-1]),element)
            if element=='(':
                bracket_counter+=1
            elif element==')':
                bracket_counter-=1

def parser(formula):
    line = ""
    variables = []
    for element in formula:
        if element not in "()∧¬∨":
            line+='('+element+')'
            variables.append(element)
        else:
            line+=element
    return rec_import_formula(line), variables

def eval(head,variables):
    for assignment in range(pow(2,len(variables))):
        solution = dict()
        b = bin(assignment)[2:]
        b = b[::-1]
        for i in range(len(variables)-1,-1,-1):
            if i<len(b):
                solution[variables[i]]=b[i]=='1'
            else:
                solution[variables[i]]=False
        if execute(solution,head):
            return True
    return False

if __name__=="__main__":
    # logical operators: ¬ ∧ ∨

    formulas = ["a∧(b∨(¬c))","(a∧(¬a))∧(b∨(¬c))","P∧(¬P)","Q∨(¬Q)"]
    for formula in formulas:
        print(formula)
        head, variables = parser(formula)
        head.print_tree()
        print(eval(head,variables),"\n\n")
