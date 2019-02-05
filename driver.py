from binaryTree import *
from postfix import *

# All expressions must be represented in this form:
#   T for True
#   F for False
#   ! for Not
#   ^ for And
#   v for Or

expression = input("Type a Boolean Expression:")
obj = Conversion(len(expression))
expression = obj.infixToPostfix(expression)

boolTree = constructTree(expression)
inorder(boolTree)
print("Size:", size(boolTree))
print("Height:", height(boolTree))
