
from lang import *
import copy

clone = copy.deepcopy

# # impl = \(p, q).(not p or q)
# impl = \
#   LambdaExpr([VarDecl("p", boolType), VarDecl("q", boolType)], OrExpr(NotExpr("p"), "q"))

# table = [
#   resolve(CallExpr(clone(impl), [True, True])),
#   resolve(CallExpr(clone(impl), [True, False])),
#   resolve(CallExpr(clone(impl), [False, True])),
#   resolve(CallExpr(clone(impl), [False, False]))
# ]

# for e in table:
#   t = check(e)
#   print(f"{e} : {t}")
#   print(evaluate(e))


e1 = resolve(AssignExpr(NewExpr(5), 3))
print(e1)
check(e1)
evaluate(e1)


