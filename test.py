
from lang import *

# (not true) and false
# e1 = AndExpr(NotExpr(BoolExpr(True)),BoolExpr(False))
#
# print(size(e1))

e = NotExpr(AndExpr(BoolExpr(True), NotExpr(BoolExpr(False))))
print(e)
print(reduce(e))
