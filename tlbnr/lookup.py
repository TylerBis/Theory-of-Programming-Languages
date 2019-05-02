from lang import *
from decorate import *

@checked
def lookup(id : str, stk : list):
  # Perform name lookup. Search the scope stack for the first
  # declaration of `id`. Returns the declaration or None if 
  # the name is undeclared.
  for scope in reversed(stk):
    if id in scope:
      return scope[id]
  return None

@checked
def resolve_unary(e : Expr, stk : list):
  resolve(e.expr, stk)
  return e

@checked
def resolve_binary(e : Expr, stk : list):
  resolve(e.lhs, stk)
  resolve(e.rhs, stk)
  return e

@checked
def resolve(e : Expr, stk : list = []):
  # Resolve references to declared variables. This requires a scope
  # stack. A scope is a mappings from names to their declarations.
  #
  # Returns the modified (in-place) tree.

  # Boolean expressions

  if type(e) is BoolExpr:
    return e

  if type(e) is AndExpr:
    return resolve_binary(e, stk)

  if type(e) is OrExpr:
    return resolve_binary(e, stk)

  if type(e) is NotExpr:
    return resolve_unary(e, stk)

  if type(e) is IfExpr:
    resolve(e.cond, stk)
    resolve(e.true, stk)
    resolve(e.false, stk)
    return e

  # Arithmetic expressions

  if type(e) is IntExpr:
    return e

  if type(e) is AddExpr:
    return resolve_binary(e, stk)

  if type(e) is SubExpr:
    return resolve_binary(e, stk)

  if type(e) is MulExpr:
    return resolve_binary(e, stk)

  if type(e) is DivExpr:
    return resolve_binary(e, stk)

  if type(e) is RemExpr:
    return resolve_binary(e, stk)

  if type(e) is NegExpr:
    return resolve_unary(e, stk)

  # Relational expressions

  if type(e) is EqExpr:
    return resolve_binary(e, stk)

  if type(e) is NeExpr:
    return resolve_binary(e, stk)

  if type(e) is LtExpr:
    return resolve_binary(e, stk)

  if type(e) is GtExpr:
    return resolve_binary(e, stk)

  if type(e) is LeExpr:
    return resolve_binary(e, stk)

  if type(e) is GeExpr:
    return resolve_binary(e, stk)

  # Lambda expressions

  if type(e) is IdExpr:
    # Perform name lookup.
    decl = lookup(e.id, stk)
    if not decl:
      raise Exception("name lookup error")

    # Bind the expression to its declaration.
    e.ref = decl
    return e

  if type(e) is LambdaExpr:
    # Create a new stack for resolving identifiers in
    # the lambda's definition.
    newstk = stk + [{var.id : var for var in e.vars}]
    resolve(e.expr, newstk)
    return e

  if type(e) is CallExpr:
    resolve(e.fn, stk)
    for a in e.args:
      resolve(e.fn, stk)
    return e

  # Reference expressions

  if type(e) is NewExpr:
    return resolve_unary(e, stk)

  if type(e) is DerefExpr:
    return resolve_unary(e, stk)

  if type(e) is AssignExpr:
    return resolve_binary(e, stk)

  print(repr(e))
  assert False
  