from lang import *

# This module implements implements small-step semantics.
#
# In particular, it implements the relation e ~> e', which
# rewrites an expression to its next smaller step. There
# are two main functions exported by the module: step, which
# performs a single transition, and reduce, which performs
# reduces an expression to a value.

def is_value(e):
  # Returns true if e denotes a value.
  return type(e) in (BoolExpr, AbsExpr, LambdaExpr)

def is_reducible(e):
  # Returns true if e can be reduced.
  return not is_value(e)

def step_and(e):
  # Compute the next step of an and-expression.
  #
  #   --------------------------- And-V
  #   v1 and v2 ~> [`v1` and `v2`]
  #
  #          e1 ~> e1'
  #   ----------------------- And-L
  #   e1 and e2 ~> e1' and e2
  #
  #          e2 ~> e2'
  #   ----------------------- And-R
  #   v1 and e2 ~> v1 and e2'
  if is_reducible(e.lhs):
    return AndExpr(step(e.lhs), e.rhs)

  if is_reducible(e.rhs):
    return AndExpr(e.lhs, step(e.rhs))

  return BoolExpr(e.lhs.val and e.rhs.val)

def step_or(e):
  # Compute the next step of an or-expression.
  #
  #          e1 ~> e1'
  #   ----------------------- Or-L
  #   e1 or e2 ~> e1' or e2
  #
  #          e2 ~> e2'
  #   ----------------------- Or-R
  #   v1 or e2 ~> v1 or e2'
  #
  #   --------------------------- Or-V
  #   v1 or v2 ~> [`v1` or `v2`]
  #
  if is_reducible(e.lhs):
    return OrExpr(step(e.lhs), e.rhs)

  if is_reducible(e.rhs):
    return OrExpr(e.lhs, step(e.rhs))

  return BoolExpr(e.lhs.val or e.rhs.val)

def step_not(e):
  # Compute the next step of a not expression.
  #
  #     e1 ~> e1'
  # ----------------- Not-1
  # not e1 ~> not e1'
  #
  # -------------------- Not-1
  # not v1 ~> [not `v1`]
  if is_reducible(e.expr):
    return NotExpr(step(e.expr))

  return BoolExpr(not e.expr.val)

def step_if(e):
  # Compute the next step of a not expression.
  #
  #                     e1 ~> e1'
  # ---------------------------------------------- Cond-1
  # if e1 then e2 else e3 ~> if e1' then e2 else e3

  # ------------------------------ Cond-true
  # if true then e2 else e3 ~> e2

  # ------------------------------ Cond-true
  # if false then e2 else e3 ~> e3

  if is_reducible(e.cond):
    return NotExpr(step(e.cond), e.true, e.false)

  if e.cond.val:
    return e.true
  else:
    return e.false

def step_app(e):
  # Apply an abstraction to an operand.
  #
  #     e1 ~> e1'
  # --------------- App-1
  # e1 e2 ~> e1' e2
  #
  #      e2 ~> e2'
  # --------------------- App-2
  # \x.e1 e2 ~> \x.e1 e2'
  #
  # ------------------- App-3
  # \x.e1 v ~> [x->v]e1
  #
  # This implements call by value.
  
  if is_reducible(e.lhs): # App-1
    return AppExpr(step(e.lhs), e.rhs)

  if type(e.lhs) is not AbsExpr:
    raise Exception("application of non-lambda")

  if is_reducible(e.rhs): # App-2
    return AppExpr(e.lhs, step(e.rhs))

  s = {
    e.lhs.var: e.rhs
  }
  return subst(e.lhs.expr, s);

def step_call(e):
  # Call a lambda function with arguments.
  #
  #                 e0 ~> e0'
  # ------------------------------------------- Call-0
  # e0(e1, e2, ..., en) ~> e0'(e1, e2, ..., en)
  #
  #                ei ~> ei'
  # ---------------------------------------- Call-i
  # (\(x1, x2, ..., xn).e0)(..., ei, ...) ~>
  #     (\(x1, x2, ..., xn).e0)(..., ei', ...)
  #
  # The rule above applies for each argument from 1 to n.
  #
  #                ei ~> ei'
  # ------------------------------------------- Call-n
  # (\(x1, x2, ..., xn).e0)(e1, e2, ..., en) ~>
  #     [x1->e1, x2->e2, ..., xn->en]e1

  if is_reducible(e.fn):
    return CallExpr(step(e.fn), e.args)

  if len(e.args) < len(e.fn.vars):
    raise Exception("too few arguments")
  if len(e.args) > len(e.fn.vars):
    raise Exception("too many arguments")

  for i in range(len(e.args)):
    if is_reducible(e.args[i]):
      return CallExpr(e.fn, e.args[:i] + [step(e.args[i])] + e.args[i+1:])

  # Map parameters to arguments.
  s = {}
  for i in range(len(e.args)):
    s[e.fn.vars[i]] = e.args[i]

  # Substitute through the definition.
  return subst(e.fn.expr, s);


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

  if type(e) is AppExpr:
    return step_app(e)

  if type(e) is CallExpr:
    return step_call(e)

  assert False

def reduce(e):
  while not is_value(e):
    e = step(e)
    print(e)
  return e
