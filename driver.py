from binaryTree import *
from postfix import *

expression = input("Type a Boolean Expression:")
obj = Conversion(len(expression))
expression = obj.infixToPostfix(expression)

boolTree = constructTree(expression)
inorder(boolTree)
