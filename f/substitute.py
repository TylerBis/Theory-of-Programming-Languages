from lang import *
from decorate import *

def subst_unary_expr(e : Expr, s : dict, T : object):
  # [x->s]@e1 = @[x->s]e1
  e1 = subst_expr(e.lhs, s)
  e2 = subst_expr(e.rhs, s)
  return T(e1, e2)

def subst_binary_expr(e : Expr, s : dict, T : object):
  # [x->s](e1 @ e2) = [x->s]e1 @ [x->s]e2
  e1 = subst_expr(e.lhs, s)
  e2 = subst_expr(e.rhs, s)
  return T(e1, e2)

def subst_exprs(es, s):
  # Substitute through a list of expressions.
  return list(map(subst_expr, es))

def subst_expr(e, s):
  # Rewrite the expression 'e' by substituting references to variables
  # in 's' with their corresponding value.
  
  if type(e) is BoolExpr:
    # [x->s]b = b
    return e

  if type(e) is AndExpr:
    return subst_binary_expr(e, s, AndExpr)

  if type(e) is OrExpr:
    return subst_binary_expr(e, s, OrExpr)

  if type(e) is NotExpr:
    return subst_unary_expr(e, s, NotExpr)

  if type(e) is IfExpr:
    # [x->s](if e1 then e2 else e3) = if [x->s]e1 then [x->s]e2 else [x->s]e3
    e1 = subst_expr(e.cond, s)
    e2 = subst_expr(e.true, s)
    e3 = subst_expr(e.false, s)
    return IfExpr(e1, e2, e3)

  # Arithmetic expressions

  if type(e) is IntExpr:
    return e

  if type(e) is AddExpr:
    return subst_binary_expr(e, s, AddExpr)

  if type(e) is SubExpr:
    return subst_binary_expr(e, s, SubExpr)

  if type(e) is MulExpr:
    return subst_binary_expr(e, s, MulExpr)

  if type(e) is DivExpr:
    return subst_binary_expr(e, s, DivExpr)

  if type(e) is RemExpr:
    return subst_binary_expr(e, s, RemExpr)

  if type(e) is NegExpr:
    return subst_unary_expr(e, s, NegExpr)

  # Relational expressions

  if type(e) is EqExpr:
    return subst_binary_expr(e, s, EqExpr)

  if type(e) is NeExpr:
    return subst_binary_expr(e, s, NeExpr)

  if type(e) is LtExpr:
    return subst_binary_expr(e, s, LtExpr)

  if type(e) is GtExpr:
    return subst_binary_expr(e, s, GtExpr)

  if type(e) is LeExpr:
    return subst_binary_expr(e, s, LeExpr)

  if type(e) is GeExpr:
    return subst_binary_expr(e, s, GeExpr)

  # Functional expressions

  if type(e) is IdExpr:
    # [x->s]x = v
    # [x->s]y = y (y != x)
    if e.ref in s:
      return s[e.ref]
    else:
      return e

  if type(e) is LambdaExpr:
    # [x->s]\(x1, x2, ...).e1 = \([x->s]x1, [x->s]x2, ...).[x->s]e1
    #
    # Note that we DO substitute through parameter types since the
    # types can be replaced during instantiation.
    # vs = list(map(lambda p: subst_type(p.type, s), e.vars))
    ps = []
    for p in e.vars:
      ps += [VarDecl(p.id, subst_type(p.type, s))]
    e1 = subst_expr(e.expr, s)
    return LambdaExpr(ps, e1)

  if type(e) is CallExpr:
    # [x->s]e1(ei) = [x->s]e1([x->s]ei)
    e = subst_expr(e.fn, s)
    es = list(map(lambda x: subst_expr(x, s), e.args))
    return CallExpr(e, es)

  # Data expressions

  if type(e) is TupleExpr:
    es = subst_exprs(e.elems, s)

  if type(e) is ProjExpr:
    e1 = subst_expr(e.obj)
    return ProjExp(e1, e.index)

  if type(e) is RecordExpr:
    fs = []
    for f in e.fields:
      e = subst_expr(f.value, s)
      fs += [FieldInit(f.id, e)]
    return RecordExpr(fs)

  if type(e) is MemberExpr:
    e1 = subst_expr(e.obj)
    return MemberExpr(e1, e.id)

  if type(e) is VariantExpr:
    assert False

  if type(e) is CaseExpr:
    assert False

  # Polymorphism expressions

  # FIXME

  assert False


def subst_type(t : Type, s : dict):
  # Substitute through the given type.

  if type(t) is BoolType:
    return t

  if type(t) is IntType:
    return t

  if type(t) is FnType:
    ts = list(map(lambda x: subst_type(x, s), t.parms))
    t = subst_type(t.ret, s)
    return FnType(ts, t)

  if type(t) is IdType:
    # [X->s]X = s
    # [X->s]Y = Y (Y != X)
    if t.ref in s:
      return s[t.ref]
    else:
      return t

  print(repr(t))
  assert False

def subst(x : object, s : dict):
  if isinstance(x, Expr):
    return subst_expr(x, s)
  if isinstance(x, Type):
    return subst_type(x, s)
  assert False