from lang import *

# Test for:
# True and not (False or True)
e = AndExpr(BoolExpr(True), NotExpr(OrExpr(BoolExpr(False), BoolExpr(True))))

print(e)
e = step_bool(e)
print(e)
e = step_bool(e)
print(e)
e = step_bool(e)
print(e)

# Test for:
# ((2 + 5) * 5) / 5
e = DivExpr(MultExpr(AddExpr(IntExpr(2), IntExpr(3)), IntExpr(5)), IntExpr(5))
print(e)
e = step_arith(e)
print(e)
e = step_arith(e)
print(e)
e = step_arith(e)
print(e)
