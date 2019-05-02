
from ast import *

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
