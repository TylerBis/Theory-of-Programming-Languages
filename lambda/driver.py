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

# \x.x
id = AbsExpr("x", IdExpr("x"))

# true = \a.\b.a
t = AbsExpr("a", AbsExpr("b", IdExpr("a")))

# false = \a.\b.b
f = AbsExpr("a", AbsExpr("b", IdExpr("b")))

# and =
land = \
  AbsExpr("p",
    AbsExpr("q",
      AppExpr(
        AppExpr(
          IdExpr("p"),
          IdExpr("q")),
        IdExpr("p"))))

e1 = AppExpr(AppExpr(land, t), f)

# print(t)
# print(f)
# print(land)
e = e1
resolve(e)
while is_reducible(e):
  e = step(e)
  print(e)
