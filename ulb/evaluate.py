from lang import *
from lookup import *

import copy

clone = copy.deepcopy

# This module implements implements big-step semantics.
#
# In particular, it implements the relation S |- e ! v (the ! is my
# approximation of the down arrow). Here, S is the runtime store,
# contains lists of bindings of variables to values of the form 
# [x1=v1, ...]. In other words, S is the call stack. Note that v
# is a value, represented by a Python object.
#
# There is one main function: evaluate, which computes the 
# value of an expression. A value is a Python object.

class Closure:
  # Represents the value of a lambda abstraction. This combines
  # the abstraction and an environment, which provides values
  # during application.
  def __init__(self, abs, env):
    self.abs = abs
    self.env = clone(env)

def eval_bool(e, store):
  # Evaluate a boolean literal:
  #
  # ---------------- E-True
  # S |- true ! True
  #
  # ------------------ E-False
  # S |- false ! False
  return e.val

def eval_and(e, store):
  # Evaluate an and-expression.
  #
  # S |- e1 ! v1   S |- e2 ! v2
  # --------------------------- E-And
  # S |- e1 and e2 ! v1 and v2
  return evaluate(e.lhs, store) and evaluate(e.rhs, store)

def eval_or(e, store):
  # Evaluate an or-expression.
  #
  # S |- e1 ! v1   S |- e2 ! v2
  # --------------------------- E-Or
  # S |- e1 or e2 ! v1 or v2
  return evaluate(e.lhs, store) or evaluate(e.rhs, store)

def eval_not(e, store):
  return not evaluate(e.expr, store)

def eval_cond(e, store):
  if evaluate(e.cond):
    return evaluate(e.true);
  else:
    return evaluate(e.false);

def eval_id(e, store):
  # Evaluate an id-expression by finding it's stored value.
  #
  # ------------- E-Id
  # S |- x ! S[x]
  return store[e.ref]

def eval_abs(e, store):
  # The evaluation of an abstraction produces a closure.
  #
  # --------------------- E-Abs
  # S |- \x.e ! <\x.e, S>
  #
  # Note that the store is cloned; it is not a reference to the current
  # store (that would cause real problems). We could also compute the
  # minimal store by finding all free variables in e and then building
  # a single mapping of those values.
  return Closure(e, store)

def eval_app(e, store):
  # Evaluate an application.
  #
  # S |- e1 ! <\x.e3, S'>   S |- e2 ! v1   S', x=v1 |- e3 ! v2
  # ---------------------------------------------------------- E-App
  #                     S |- e1 e2 ! v2
  #
  # In other words, evaluate the LHS and RHS. Use the environment
  # of the closure (S'), along with the new variable binding to
  # evaluate the closure's body.
  #
  # Note that this does not handle recursion correctly because the 
  # store flat. 
  c = evaluate(e.lhs, store)

  if type(c) is not Closure:
    raise Exception("cannot apply a non-closure to an argument")

  v = evaluate(e.rhs, store)

  return evaluate(c.abs.expr, c.env + {c.abs.var: v})

def eval_lambda(e, store):
  # The evaluation of a lambda abstraction produces a closure.
  #
  # ----------------------------------------------------- E-Lambda
  # S |- \(x1, x2, ..., xn).e ! <\(x1, x2, ..., xn).e, S>
  return Closure(e, store)

def eval_call(e, store):
  c = evaluate(e.fn, store)
  
  if type(c) is not Closure:
    raise Exception("cannot apply a non-closure to an argument")

  # Evaluate arguments
  args = []
  for a in e.args:
    args += [evaluate(a, store)]

  # Build the new environment.
  env = clone(c.env)
  for i in range(len(args)):
    env[c.abs.vars[i]] = args[i]

  return evaluate(c.abs.expr, env)

def evaluate(e, store = {}):
  # Evaluate an expression. The store is a stack of mappings from
  # variables to values.

  if type(e) is BoolExpr:
    return eval_bool(e, store)

  if type(e) is AndExpr:
    return eval_and(e, store)

  if type(e) is OrExpr:
    return eval_or(e, store)

  if type(e) is NotExpr:
    return eval_not(e, store)

  if type(e) is IdExpr:
    return eval_id(e, store)

  if type(e) is AbsExpr:
    return eval_abs(e, store)

  if type(e) is AppExpr:
    return eval_app(e, store)

  if type(e) is LambdaExpr:
    return eval_lambda(e, store)

  if type(e) is CallExpr:
    return eval_call(e, store)
