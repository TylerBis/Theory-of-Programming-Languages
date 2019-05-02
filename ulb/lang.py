
class Expr:
  # Represents the set of expressions in the
  # pure (or untyped) lambda calculus. This is
  # defined as:
  # 
  #   e ::= b                     -- boolean literals (true, false)
  #         e1 and e2             -- logical ands
  #         e1 or e2              -- logical ors
  #         not e1                -- logical nots
  #         if e1 then e2 else e3 -- conditionals
  #         x                     -- variables
  #         \x.e1                 -- abstractions
  #         e1 e2                 -- applications
  #         \(x1, x2, ..., xn).e1 -- lambda expressions
  #         e0(e1, e2, ..., en)   -- call expressions
  #         _                     -- Placeholders
  pass

class BoolExpr(Expr):
  # Represents the literals 'true' and 'false'.
  def __init__(self, val):
    self.val = val

  def __str__(self):
    return "true" if self.val else "false"

class AndExpr(Expr):
  # Represents expressions of the form `e1 and e2`.
  def __init__(self, e1, e2):
    self.lhs = expr(e1)
    self.rhs = expr(e2)

  def __str__(self):
    return f"({self.lhs} and {self.rhs})"

class OrExpr(Expr):
  # Represents expressions of the form `e1 or e2`.
  def __init__(self, e1, e2):
    self.lhs = expr(e1)
    self.rhs = expr(e2)

  def __str__(self):
    return f"({self.lhs} or {self.rhs})"

class NotExpr(Expr):
  # Represents expressions of the form `not e1`.
  def __init__(self, e1):
    self.expr = expr(e1)

  def __str__(self):
    return f"(not {self.expr})"

class IfExpr(Expr):
  # Represents expressions of the form `if e1 then e2 else e3`.
  def __init__(self, e1, e2, e3):
    self.cond = expr(e1)
    self.true = expr(e2)
    self.false = expr(e3)

  def __str__(self):
    return f"(if {self.cond} then {self.true} else {self.false})"

class IdExpr(Expr):
  # Represents identifiers that refer to variables.
  def __init__(self, x):
    if type(x) is str:
      # Initialized by an unresolved string.
      self.id = x
      self.ref = None # Eventually links to a var
    elif type(x) is VarDecl:
      # Initialized by a known variable.
      self.id = x.id
      self.ref = x

  def __str__(self):
    return self.id

class VarDecl:
  # Represents the declaration of a variable.
  # 
  # Note that this is NOT an expression. It is
  # the declaration of a name.
  def __init__(self, id):
    self.id = id

  def __str__(self):
    return self.id

class AbsExpr(Expr):
  # Represents lambda abstractions of the form '\x.e1'.
  def __init__(self, var, e1):
    self.var = decl(var)
    self.expr = expr(e1)

  def __str__(self):
    return f"\\{self.var}.{self.expr}"

class AppExpr(Expr):
  # Represents applications of the form 'e1 e2'
  def __init__(self, e1, e2):
    self.lhs = expr(e1)
    self.rhs = expr(e2)

  def __str__(self):
    return f"({self.lhs} {self.rhs})"

class LambdaExpr(Expr):
  # Represents multi-argument lambda abstractions.
  # Note that '\(x, y, z).e' is syntactic sugar for
  # '\x.\y.\z.e'.
  def __init__(self, vars, e1):
    self.vars = list(map(decl, vars))
    self.expr = expr(e1)

  def __str__(self):
    parms = ",".join(str(v) for v in self.vars)
    return f"\\({parms}).{self.expr}"

class CallExpr(Expr):
  # Represents calls of multi-argument lambda 
  # abstractions.
  def __init__(self, fn, args):
    self.fn = expr(fn)
    self.args = list(map(expr, args))

  def __str__(self):
    args = ",".join(str(a) for a in self.args)
    return f"{self.fn} ({args})"

class PlaceholderExpr(Expr):
  # Represents a placeholder for an argument to a call.
  def __str__(self):
    return "_"

def expr(x):
  # Turn a Python object into an expression. This is solely
  # used to make simplify the writing expressions.
  if type(x) is bool:
    return BoolExpr(x)
  if type(x) is str:
    return IdExpr(x)
  return x

def decl(x):
  # Turn a python object into a declaration.
  if type(x) is str:
    return VarDecl(x)
  return x

from lookup import resolve
from subst import subst
from reduce import step, reduce
from evaluate import evaluate
from curry import curry
