from lang import *
from decorate import *

def inst_unary_expr(e : Expr, s : dict, T : object):
  e1 = instantiate(e.expr)
  return T(e1)

def inst_binary_expr(e : Expr, s : dict, T : object):
  e1 = instantiate(e.lhs)
  e2 = instantiate(e.rhs)
  return T(e1, e2)

def instantiate(e : Expr, s : dict = {}):
  # Instantiate the given expression by applying instantiation
  # expressions.
  #
  # For the most part, this simply returns the node given. For
  # instantiation expressions, we apply substitution.
  #
  # This is is closely related to reduction except that the only
  # "evaluation we perform is instantiation of generics with
  # type arguments.

  # Boolean expressions

  if type(e) is BoolExpr:
    return e

  if type(e) is AndExpr:
    return inst_binary_expr(e, s, AndExpr)

  if type(e) is OrExpr:
    return inst_binary_expr(e, s, OrExpr)

  if type(e) is NotExpr:
    return inst_unary_expr(e, s, NotExpr)

  if type(e) is IfExpr:
    e1 = instantiate(e.cond, s)
    e2 = instantiate(e.true, s)
    e3 = instantiate(e.false, s)
    return IfExpr(e1, e2, e3)

  # Arithmetic expressions

  if type(e) is IntExpr:
    return e

  if type(e) is AddExpr:
    return inst_binary_expr(e, s, AddExpr)

  if type(e) is SubExpr:
    return inst_binary_expr(e, s, SubExpr)

  if type(e) is MulExpr:
    return inst_binary_expr(e, s, MulExpr)

  if type(e) is DivExpr:
    return inst_binary_expr(e, s, DivExpr)

  if type(e) is RemExpr:
    return inst_binary_expr(e, s, RemExpr)

  if type(e) is NegExpr:
    return subst_unary_expr(e, s, NegExpr)

  # Relational expressions

  if type(e) is EqExpr:
    return inst_binary_expr(e, s, EqExpr)

  if type(e) is NeExpr:
    return inst_binary_expr(e, s, NeExpr)

  if type(e) is LtExpr:
    return inst_binary_expr(e, s, LtExpr)

  if type(e) is GtExpr:
    return inst_binary_expr(e, s, GtExpr)

  if type(e) is LeExpr:
    return inst_binary_expr(e, s, LeExpr)

  if type(e) is GeExpr:
    return inst_binary_expr(e, s, GeExpr)

  # Functional expressions

  if type(e) is IdExpr:
    # Return a new unbound id expression.
    return IdExpr(e.id)

  if type(e) is LambdaExpr:
    # Build new parameters for the lambda expression.
    ps = list(map(lambda p: VarDecl(p.id, p.type), e.vars))
    e1 = instantiate(e.expr, s)
    return LambdaExpr(e.vars, e1)

  if type(e) is CallExpr:
    e = instantiate(e.fn, s)
    es = list(map(lambda x: instantiate(x, s), e.args))
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

  # Polymorphic expressions

  if type(e) is GenericExpr:
    # A generic is a value, just return it.
    #
    # FIXME: How do we deal with closures in this context? Or is that
    # managed by the substitution rules.
    return e

  if type(e) is InstExpr:
    # Recursively instantiate the generic... This *should* produce a
    # GenericExpr on the left, even if that was computed by another 
    # GenericExpr.
    gen = instantiate(e.gen)
    assert type(gen) is GenericExpr
    assert len(gen.vars) == len(e.args)

    # Build the parameter mapping.
    sub = {}
    for i in range(len(e.args)):
      sub[gen.vars[i]] = e.args[i]

    # Substitute through the expression to produce the instantiated
    # form. Note that this the result is unresolved and untyped.
    return subst(gen.expr, sub)

  print(repr(e))
  raise Exception("unknown expression")
