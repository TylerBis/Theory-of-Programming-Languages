
from lang import *
import copy

clone = copy.deepcopy

print("---- types ----")
f1 = resolve(FnType([int, int], bool))
print(f1)

r1 = resolve(RefType(int))
print(r1)

t1 = resolve(TupleType([int, bool, int, f1]))
print (t1)

t2 = resolve(RecordType([("x", int), ("y", int), ("z", bool)]))
print(t2)

t3 = resolve(VariantType([("x", int), ("y", int), ("z", bool)]))
print(t3)

t4 = resolve(UniversalType(["X", "Y"], FnType(["X"], "X")))
print(t4)

t5 = resolve(ExistentialType(["X"], RecordType([("x", "X")])))
print(t5)

print("---- exprs ----")
# e1 = resolve(TupleExpr([0, 1, True]))
# check(e1)
# print(f"* expr:  {e1}")
# print(f"* value: {evaluate(e1)}")

# e2 = resolve(ProjExpr(clone(e1), 1))
# check(e2)
# print(f"* expr:  {e2}")
# print(f"* value: {evaluate(e2)}")

# e3 = resolve(RecordExpr([("x", 0), ("y", True), ("z", 42)]))
# check(e3)
# print(f"* expr:  {e3}")
# print(f"* value: {evaluate(e3)}")

# e4 = resolve(MemberExpr(clone(e3), "x"))
# check(e4)
# print(f"* expr:  {e4}")
# print(f"* value: {evaluate(e4)}")

# try:
#   e5 = resolve(MemberExpr(clone(e3), "q"))
#   check(e5)
# except:
#   pass

# e6 = resolve(RecordExpr([("a", clone(e3))]))
# check(e6)
# print(f"* expr:  {e6}")
# print(f"* value: {evaluate(e6)}")

# e7 = MemberExpr(MemberExpr(e6, "a"), "y")
# check(e7)
# print(f"* expr:  {e7}")
# print(f"* value: {evaluate(e7)}")

# e8 = resolve(VariantExpr(("x", 3), t3))
# check(e8)
# print(f"* expr:  {e8}")
# print(f"* value: {evaluate(e8)}")

# try:
#   e9 = resolve(VariantExpr(("foo", 3), t3))
#   check(e9)
# except:
#   pass

# e10 = resolve(CaseExpr(clone(e8), [
#   ("x", "a", True),
#   ("y", "b", False),
# ]))
# check(e10)
# print(f"* expr:  {e10}")
# print(f"* value: {evaluate(e10)}")

x1 = LambdaExpr([("a", "T"), ("b", "U")], LtExpr("a", "b"))
x2 = GenericExpr(["T", "U"], x1)
e11 = resolve(clone(x2))
print(f"* expr:  {e11}")
print(f"* type:  {check(e11)}")

e12 = resolve(InstExpr(clone(x2), [int, int]))
print(f"* expr:  {e12}")
print(f"* type:  {check(e12)}")
e12 = resolve(instantiate(e12))
print(f"* expr 0:  {e12}")
print(f"* type 0:  {check(e12)}")


