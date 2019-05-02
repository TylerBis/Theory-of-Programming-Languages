from lang import *

def curry_unary(e, Node):
  return Node(curry(e.expr))

def curry_binary(e, Node):
  return Node(curry(e.lhs), curry(e.rhs))

def curry_app(e):
  # Applying a placeholder to an application simply
  # yields the lambda expression. That is:
  #
  #   (\x.x) _
  #
  # Produces \x.x.
  if type(e.rhs) is PlaceholderExpr:
    return e.lhs
  return curry_binary(e, AppExpr)

def find_placeholders(args):
  phs = []
  for i in range(len(args)):
    if type(args[i]) is PlaceholderExpr:
      phs += [i]
  return phs

def curry_call(e):
  # Calling a lambda with one or more placeholders yields a 
  # new function that calls the previous function with the 
  # provided operands. For example:
  #
  #   (\(x, y, z).if x then y else z) (_, true, false)
  #
  # Yields:
  #
  #   (\(x').((\(x, y, z).if x then y else z) (x', true, false)))
  #
  # Note that we can't just replace the previous lambda with
  # a new call. If we try this, we might have to evaluate the
  # operands ahead of time, which seems unfortunate since
  # currying isn't really a form of evaluation (although it
  # could be in small-step semantics). We could simply substitute
  # arguments as in call-by-name, but that leads to other issues
  # related to name bindings (i.e., we might move an expression
  # outside of its binding context).
  #
  # Also, be aware that the formation of this lambda expression
  # may capture non-local ids in the arguments of the call;
  # we'll need to form closures during evaluation.

  # Get indexes of all placeholders
  phs = find_placeholders(e.args)

  # If there are no placeholders, curry operands.
  if not phs:
    return CallExpr(e.fn.vars, list(map(curry, e.args)))

  # FIXME: We still need to curry non-placeholder
  # arguments if there are, in fact placeholders.

  # Build a new sequence of variables and replace corresponding
  # placeholders
  vars = []
  for i in phs:
    vars += [VarDecl("_" + e.fn.vars[i].id)]

  # Rebuild the arguments by replacing placeholders with
  # arguments. We do this in place rather than building
  # a new list of arguments (it's a little easier to implement).
  n = 0 # Current variable index.
  for i in phs:
    e.args[i] = IdExpr(vars[n])
    n += 1

  # Wrap the original call with a new lambda expression.
  return LambdaExpr(vars, e)

def curry(e):
  # Rewrite e so that any calls involving placeholders are
  # rewritten to yield new lambda expressions.

  if type(e) is BoolExpr:
    return e

  if type(e) is AndExpr:
    return curry_binary(e, AndExpr)

  if type(e) is OrExpr:
    return curry_binary(e, AndExpr)

  if type(e) is NotExpr:
    return curry_unary(e, AndExpr)

  if type(e) is IfExpr:
    return IfExpr(curry(e.cond), curry(e.true), curry(e.false))

  if type(e) is IdExpr:
    return e

  if type(e) is AbsExpr:
    return AbsExpr(e.var, curry(e.expr))

  if type(e) is AppExpr:
    return curry_app(e)

  if type(e) is LambdaExpr:
    return LambdaExpr(e.vars, curry(e.expr))

  if type(e) is CallExpr:
    return curry_call(e)

  assert False