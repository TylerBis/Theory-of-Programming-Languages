# Taken from GeeksforGeeks (modified)
# Python program for expression tree
"""Implement the AST for the following language:

e ::= true | false | not e1 | e1 and e2 | e1 or e2

Implement the following operations on the abstract syntax tree:

size -- compute the size of an expression
height -- compute the height of an expression
same -- Return true if two expressions are identical
value -- compute the value of an expression
step -- Return an expression representing a single step of evaluation
reduce -- Calls step repeatedly until the expression is non-reducible"""
# An expression tree node
class Expr:

    # Constructor to create a node
    def __init__(self , value):
        self.value = value
        self.left = None
        self.right = None

# A utility function to check if 'c'
# is an operator
def isOperator(c):
    if (c == '!' or c == '^' or c == 'v'):
        return True
    else:
        return False

# A utility function to do inorder traversal
def inorder(e):
    if e is not None:
        inorder(e.left)
        print(e.value)
        inorder(e.right)

def postorder(e):
    if e is not None:
        postorder(e.left)
        postorder(e.right)
        print(e.value)

def preorder(e):
    if e is not None:
        print(e.value)
        preorder(e.left)
        preorder(e.right)

# Computes the size of an expression
def size(e):
    pass

# Computes height of an expression
def height(e):
    pass

# Return true if two expressions are identical
def same(e):
    pass

# Computes the value of an expression
def val(e):
    pass

# Return an expression representing a single step of evaluation
def step(e):
    pass

# Calls step repeatedly until the expression is non-reducible
def reduce(e):
    pass

# Returns root of constructed tree for
# given postfix expression
def constructTree(postfix):
    stack = []

    # Traverse through every character of input expression
    for char in postfix:

        # if operand, simply push into stack
        if char == 'T':
            e = Expr('T')
            stack.append(e)

        elif char == 'F':
            e = Expr('F')
            stack.append(e)
		# Operator
        elif isOperator(char):

            # Pop two top nodes
            e = Expr(char)
            e1 = stack.pop()
            e2 = stack.pop()

			# make them children
            e.right = e1
            e.left = e2

            # Add this subexpression to stack
            stack.append(e)
        else:
            pass
    # Only element will be the root of expression tree
    e = stack.pop()

    return e

# Driver program to test above
# postfix = "ab+ef*g*-"
# r = constructTree(postfix)
# print "Infix expression is"
# inorder(r)
