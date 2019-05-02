
class Expr:
  # Represents the set of expressions in the
  # pure (or untyped) lambda calculus. This is
  # defined as:
  # 
  #   e ::= x                     -- variables
  #         \\x.e1                -- abstractions
  #         e1 e2                 -- application
  #         \(x1, x2, ..., xn).e1 -- lambda expression
  #         e0(e1, e2, ..., en)   -- call expression
  pass

class IdExpr(Expr):
  """Represents identifiers that refer to
  variables."""
  def __init__(self, id):
    self.id = id
    self.ref = None

  def __str__(self):
    return self.id

class VarDecl:
  """Represents the declaration of a variable.

  Note that this is NOT an expression. It is
  the declaration of a name."""
  def __init__(self, id):
    self.id = id

  def __str__(self):
    return self.id

class AbsExpr(Expr):
  # Represents lambda abstractions of the form '\x.e1'.
  def __init__(self, var, e1):
    if type(var) is str:
      self.var = VarDecl(var)
    else:
      self.var = var
    self.expr = e1

  def __str__(self):
    return f"\\{self.var}.{self.expr}"

class AppExpr(Expr):
  # Represents applications of the form 'e1 e2'
  def __init__(self, lhs, rhs):
    self.lhs = lhs
    self.rhs = rhs

  def __str__(self):
    return f"({self.lhs} {self.rhs})"

class LambdaExpr(Expr)
  # Represents multi-argument lambda abstractions.
  # Note that '\(x, y, z).e' is syntactic sugar for
  # '\x.\y.\z.e'.
  def __init__(self, vars, e1):
    self.vars = []
    for v in vars:
    if type(var) is str:
      self.vars[] += [VarDecl(var)]
    else:
      self.vars += [var]
    self.expr = e1

  def __str__(self):
    return f"\\({",".join([str(v) for v in self.vars])}).{self.expr}"

class CallExpr:
  # Represents calls of multi-argument lambda 
  # abstractions.
  def __init__(self, fn, args):
    self.fn = fn
    self.args = args

def is_value(e):
  return type(e) in (IdExpr, AbsExpr, LambdaExpr)

def is_reducible(e):
  return not is_value(e)

def resolve(e, scope = []):
  if type(e) is AppExpr:
    resolve(e.lhs, scope)
    resolve(e.rhs, scope)
    return

  if type(e) is AbsExpr:
    # \x.e -- Add x to scope, recurse through e
    # (\x.e) x
    resolve(e.expr, scope + [e.var])
    return

  if type(e) is IdExpr:
    for var in reversed(scope):
      if e.id == var.id:
        e.ref = var # Bind id to declaration
        return
    raise Exception("name lookup error")

  # print(type(e))
  assert False

def subst(e, s):
  # [x->v]x = v
  # [x->v]y = y (y != x)
  if type(e) is IdExpr:
    if e.ref in s: # FIXME: This is wrong.
      return s[e.ref]
    else:
      return e

  # [x->v] \x.e1 = \x.[x->v]e1
  if type(e) is AbsExpr:
    return AbsExpr(e.var, subst(e.expr, s))

  if type(e) is AppExpr:
    return AppExpr(subst(e.lhs, s), subst(e.rhs, s))

  assert False

def step_app(e):
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

def step(e):
  assert isinstance(e, Expr)
  assert is_reducible(e)

  if type(e) is AppExpr:
    return step_app(e)

  assert False


