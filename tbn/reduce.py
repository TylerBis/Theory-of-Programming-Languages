from lang import *

# This module implements implements small-step semantics.
#
# In particular, it implements the relation e ~> e', which
# rewrites an expression to its next smaller step. There
# are two main functions exported by the module: step, which
# performs a single transition, and reduce, which performs
# reduces an expression to a value.

def is_value(e):
  # Returns true if the expression is designated as a value (i.e., 
  # that the expression is irreducible).
  return type(e) in (BoolExpr, IntExpr)

def is_reducible(e):
  # Returns true if the expression is reducible.
  return not is_value(e)

def step_unary(e, Node, op):
  # Compute the next step of a unary expression.
  #
  #     e1 ~> e1'
  # ----------------- Not-1
  # op e1 ~> op e1'
  #
  # ----------------- Not-1
  # op v1 ~> [op `v1`]
  if is_reducible(e.expr):
    return Node(step(e.expr))

  return expr(op(e.expr.value))

def step_binary(e, Node, op):
  # Compute the next step of a binary expression.
  #
  #   ---------------------------
  #   v1 op v2 ~> [`v1` op `v2`]
  #
  #          e1 ~> e1'
  #   -----------------------
  #   e1 op e2 ~> e1' op e2
  #
  #          e2 ~> e2'
  #   -----------------------
  #   v1 op e2 ~> v1 op e2'
  
  # LHS first
  if is_reducible(e.lhs):
    return Node(step(e.lhs), e.rhs)

  # RHS next
  if is_reducible(e.rhs):
    return Node(e.lhs, step(e.rhs))

  # Combine the results.
  return expr(op(e.lhs.value, e.rhs.value))

def step_and(e):
  return step_binary(e, AndExpr, lambda x, y: x and y)

def step_or(e):
  return step_binary(e, OrExpr, lambda x, y: x or y)

def step_not(e):
  return step_unary(e, NotExpr, lambda x: not x)

def step_if(e):
  # Compute the next step of a not expression.
  #
  #                     e1 ~> e1'
  # ---------------------------------------------- Cond-1
  # if e1 then e2 else e3 ~> if e1' then e2 else e3
  #
  # ------------------------------ Cond-true
  # if true then e2 else e3 ~> e2
  #
  # ------------------------------ Cond-true
  # if false then e2 else e3 ~> e3
  #
  # Note that this selects either e2 or e3, but does not "advance"
  # the selected expression.

  if is_reducible(e.cond):
    return NotExpr(step(e.cond), e.true, e.false)

  if e.cond.val:
    return e.true
  else:
    return e.false

def step_add(e):
  return step_binary(e, AddExpr, lambda x, y: x + y)

def step_sub(e):
  return step_binary(e, SubExpr, lambda x, y: x - y)

def step_mul(e):
  return step_binary(e, MulExpr, lambda x, y: x * y)

def step_div(e):
  return step_binary(e, DivExpr, lambda x, y: x / y)

def step_rem(e):
  return step_binary(e, RemExpr, lambda x, y: x % y)

def step_eq(e):
  return step_binary(e, EqExpr, lambda x, y: x == y)

def step_ne(e):
  return step_binary(e, NeExpr, lambda x, y: x != y)

def step_lt(e):
  return step_binary(e, LtExpr, lambda x, y: x < y)

def step_gt(e):
  return step_binary(e, GtExpr, lambda x, y: x > y)

def step_le(e):
  return step_binary(e, LeExpr, lambda x, y: x <= y)

def step_ge(e):
  return step_binary(e, GeExpr, lambda x, y: x >= y)

def step(e):
  assert isinstance(e, Expr)
  assert is_reducible(e)

  if type(e) is AndExpr:
    return step_and(e)

  if type(e) is OrExpr:
    return step_or(e)

  if type(e) is NotExpr:
    return step_not(e)

  if type(e) is IfExpr:
    return step_if(e)

  if type(e) is AddExpr:
    return step_add(e)

  if type(e) is SubExpr:
    return step_sub(e)

  if type(e) is MulExpr:
    return step_mul(e)

  if type(e) is DivExpr:
    return step_div(e)

  if type(e) is RemExpr:
    return step_rem(e)

  if type(e) is NegExpr:
    return step_neg(e)

  if type(e) is EqExpr:
    return step_eq(e)

  if type(e) is NeExpr:
    return step_ne(e)

  if type(e) is LtExpr:
    return step_lt(e)

  if type(e) is GtExpr:
    return step_gt(e)

  if type(e) is LeExpr:
    return step_le(e)

  if type(e) is GeExpr:
    return step_ge(e)

  assert False

def reduce(e):
  while not is_value(e):
    e = step(e)
    print(e)
  return e
