from lang import *

# This module implements implements big-step semantics.

def eval_bool(e):
  return e.value

def eval_and(e):
  return evaluate(e.lhs) and evaluate(e.rhs)

def eval_or(e):
  return evaluate(e.lhs) or evaluate(e.rhs)

def eval_not(e):
  return not evaluate(e.expr)

def eval_if(e):
  if evaluate(e.cond):
    return evaluate(e.true);
  else:
    return evaluate(e.false);

def eval_int(e):
  return e.value

def eval_add(e):
  return evaluate(e.lhs) + evaluate(e.rhs)

def eval_sub(e):
  return evaluate(e.lhs) - evaluate(e.rhs)

def eval_mul(e):
  return evaluate(e.lhs) * evaluate(e.rhs)

def eval_div(e):
  return evaluate(e.lhs) / evaluate(e.rhs)

def eval_rem(e):
  return evaluate(e.lhs) % evaluate(e.rhs)

def eval_neg(e):
  return -evaluate(e.expr)

def eval_eq(e):
  return evaluate(e.lhs) == evaluate(e.rhs)

def eval_ne(e):
  return evaluate(e.lhs) != evaluate(e.rhs)

def eval_lt(e):
  return evaluate(e.lhs) < evaluate(e.rhs)

def eval_gt(e):
  return evaluate(e.lhs) > evaluate(e.rhs)

def eval_le(e):
  return evaluate(e.lhs) <= evaluate(e.rhs)

def eval_ge(e):
  return evaluate(e.lhs) >= evaluate(e.rhs)

def evaluate(e):
  assert isinstance(e, Expr)

  if type(e) is BoolExpr:
    return eval_bool(e)

  if type(e) is AndExpr:
    return eval_and(e)

  if type(e) is OrExpr:
    return eval_or(e)

  if type(e) is NotExpr:
    return eval_not(e)

  if type(e) is IfExpr:
    return eval_if(e)

  if type(e) is IntExpr:
    return eval_int(e)

  if type(e) is AddExpr:
    return eval_add(e)

  if type(e) is SubExpr:
    return eval_sub(e)

  if type(e) is MulExpr:
    return eval_mul(e)

  if type(e) is DivExpr:
    return eval_div(e)

  if type(e) is RemExpr:
    return eval_rem(e)

  if type(e) is NegExpr:
    return eval_neg(e)

  if type(e) is EqExpr:
    return eval_eq(e)

  if type(e) is NeExpr:
    return eval_ne(e)

  if type(e) is LtExpr:
    return eval_lt(e)

  if type(e) is GtExpr:
    return eval_gt(e)

  if type(e) is LeExpr:
    return eval_le(e)

  if type(e) is GeExpr:
    return eval_ge(e)

  assert False
