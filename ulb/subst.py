from lang import *

def subst(e, s):
  # Rewrite the expression 'e' by substituting references to variables
  # in 's' with their corresponding value.
  
  if type(e) is BoolExpr:
    # [x->s]b = b
    return e

  if type(e) is AndExpr:
    # [x->s](e1 and e2) = [x->s]e1 and [x->s]e2
    e1 = subst(e.lhs, s)
    e2 = subst(e.rhs, s)
    return AndExpr(e1, e2)

  if type(e) is OrExpr:
    # [x->s](e1 or e2) = [x->s]e1 or [x->s]e2
    e1 = subst(e.lhs, s)
    e2 = subst(e.rhs, s)
    return OrExpr(e1, e2)

  if type(e) is NotExpr:
    # [x->s](not e1) = not [x->s]e1
    e1 = subst(e.expr, s)
    return NotExpr(e1)

  if type(e) is IfExpr:
    # [x->s](if e1 then e2 else e3) = if [x->s]e1 then [x->s]e2 else [x->s]e3
    e1 = subst(e.cond, s)
    e2 = subst(e.true, s)
    e3 = subst(e.false, s)
    return IfExpr(e1, e2, e3)

  if type(e) is IdExpr:
    # [x->s]x = v
    # [x->s]y = y (y != x)
    if e.ref in s:
      return s[e.ref]
    else:
      return e

  if type(e) is AbsExpr:
    # [x->s] \x.e1 = \x.[x->s]e1
    #
    # Note that references to var  will never be replaced, so the
    # binding will be preserved when we create the expression.
    #
    # Alternatively, we could create a new variable and redo 
    # resolution on the resulting expression.
    e1 = subst(e.expr, s)
    return AbsExpr(e.var, e1)

  if type(e) is AppExpr:
    # [x->s](e1 e2) = [x->s]e1 [x->s]e2
    e1 = subst(e.lhs, s)
    e2 = subst(e.rhs, s)
    return AppExpr(e1, e2)

  if type(e) is LambdaExpr:
    # [x->s]\(x1, x2, ...).e1 = \(x1, x2, ...).[x->s]e1
    e1 = subst(e.expr, s)
    return LambdaExpr(e.vars, e1)

  if type(e) is CallExpr:
    # [x->s]e0(e1, e2, ...)
    e0 = subst(e.fn, s)
    args = list(map(lambda x: subst(x, s), e.args))
    return CallExpr(e0, args)

  assert False
