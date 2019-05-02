
class Type:
  # Represents a type in the language.
  #
  # T ::= Bool
  #       Int
  #       (T1, T2, ..., Tn) -> T0
  #       Ref T1
  pass

class BoolType(Type):
  # Represents the type 'Bool'
  def __str__(self):
    return "Bool"

class IntType(Type):
  # Represents the type 'Int'
  def __str__(self):
    return "Int"

class FnType(Type):
  # Represents types of the form '(T1, T2, ..., Tn) -> T0'
  def __init__(self, parms, ret):
    self.parms = parms
    self.ret = ret

class RefType(Type):
  # Represents types of the form `Ref T1`.
  def __init__(self, t):
    self.ref = t

# The (only) boolean type
boolType = BoolType()

# The (only) integer type
intType = IntType()

# Expressions

class Expr:
  # Represents the set of expressions.
  # 
  #   e ::= B -- boolean expressions
  #         Z -- arithmetic expressions
  #         L -- lambda expressions
  #         R -- reference expressions
  #
  #   B ::= true
  #         false
  #         e1 and e2
  #         e1 or e2
  #         not e1
  #         e1 ? e2 : e3
  #
  #   Z ::= n
  #         ...
  #
  #   L ::= x
  #         \(x1:T1, x2:T2, ..., xn:Tn).e1
  #         e0(e1, e2, ..., en)
  #
  #   R ::= new e1
  #         *e1
  #         e1 = e2
  
  def __init__(self):
    self.type = None

## Boolean expressions

class BoolExpr(Expr):
  # Represents the literals 'true' and 'false'.
  def __init__(self, val):
    Expr.__init__(self)
    self.value = val

  def __str__(self):
    return "true" if self.val else "false"

class AndExpr(Expr):
  # Represents expressions of the form `e1 and e2`.
  def __init__(self, e1, e2):
    Expr.__init__(self)
    self.lhs = expr(e1)
    self.rhs = expr(e2)

  def __str__(self):
    return f"({self.lhs} and {self.rhs})"

class OrExpr(Expr):
  # Represents expressions of the form `e1 or e2`.
  def __init__(self, e1, e2):
    Expr.__init__(self)
    self.lhs = expr(e1)
    self.rhs = expr(e2)

  def __str__(self):
    return f"({self.lhs} or {self.rhs})"

class NotExpr(Expr):
  # Represents expressions of the form `not e1`.
  def __init__(self, e1):
    Expr.__init__(self)
    self.expr = expr(e1)

  def __str__(self):
    return f"(not {self.expr})"

class IfExpr(Expr):
  # Represents expressions of the form `if e1 then e2 else e3`.
  def __init__(self, e1, e2, e3):
    Expr.__init__(self)
    self.cond = expr(e1)
    self.true = expr(e2)
    self.false = expr(e3)

  def __str__(self):
    return f"(if {self.cond} then {self.true} else {self.false})"

## Id expressions

class IdExpr(Expr):
  # Represents identifiers that refer to variables.
  def __init__(self, x):
    Expr.__init__(self)
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

## Integer expressions

class IntExpr(Expr):
  # Represents numeric literals.
  def __init__(self, val):
    Expr.__init__(self)
    self.value = val

  def __str__(self):
    return str(self.value)

class AddExpr(Expr):
  # Represents expressions of the form `e1 + e2`.
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} + {self.rhs})"

class SubExpr(Expr):
  # Represents expressions of the form `e1 + e2`.
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} + {self.rhs})"

class MulExpr(Expr):
  # Represents expressions of the form `e1 - e2`.
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} - {self.rhs})"

class DivExpr(Expr):
  # Represents expressions of the form `e1 / e2`.
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} / {self.rhs})"

class RemExpr(Expr):
  # Represents expressions of the form `e1 % e2`.
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} % {self.rhs})"

class NegExpr(Expr):
  # Represents expressions of the form `-e1`.
  def __init__(self, e1):
    Expr.__init__(self)
    self.expr = expr(e1)

  def __str__(self):
    return f"(-{self.expr})"

## Relational expressions

class EqExpr(Expr):
  # Represents expressions of the form `e1 == e2`.
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} == {self.rhs})"

class NeExpr(Expr):
  # Represents expressions of the form `e1 != e2`.
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} != {self.rhs})"

class LtExpr(Expr):
  # Represents expressions of the form `e1 < e2`.
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} < {self.rhs})"

class GtExpr(Expr):
  # Represents expressions of the form `e1 > e2`.
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} > {self.rhs})"

class LeExpr(Expr):
  # Represents expressions of the form `e1 <= e2`.
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} <= {self.rhs})"

class GeExpr(Expr):
  # Represents expressions of the form `e1 >= e2`.
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} >= {self.rhs})"

## Lambda terms

class VarDecl:
  # Represents the declaration of a variable.
  # 
  # Note that this is NOT an expression. It is
  # the declaration of a name.
  def __init__(self, id, t):
    Expr.__init__(self)
    self.id = id
    self.type = t

  def __str__(self):
    return self.id

class LambdaExpr(Expr):
  # Represents multi-argument lambda abstractions.
  # Note that '\(x, y, z).e' is syntactic sugar for
  # '\x.\y.\z.e'.
  def __init__(self, vars, e1):
    Expr.__init__(self)
    self.vars = list(map(decl, vars))
    self.expr = expr(e1)

  def __str__(self):
    parms = ",".join(str(v) for v in self.vars)
    return f"\\({parms}).{self.expr}"

class CallExpr(Expr):
  # Represents calls of multi-argument lambda 
  # abstractions.
  def __init__(self, fn, args):
    Expr.__init__(self)
    self.fn = expr(fn)
    self.args = list(map(expr, args))

  def __str__(self):
    args = ",".join(str(a) for a in self.args)
    return f"{self.fn} ({args})"

class PlaceholderExpr(Expr):
  def __init__(self):
    Expr.__init__(self)

  # Represents a placeholder for an argument to a call.
  def __str__(self):
    return "_"

## Reference expressions

class NewExpr(Expr):
  # Represents the allocation of new objects.
  def __init__(self, e):
    Expr.__init__(self)
    self.expr = expr(e)

  def __str__(self):
    return f"new {self.expr}"

class DerefExpr(Expr):
  # Returns the value at a location.
  def __init__(self, e):
    Expr.__init__(self)
    self.expr = expr(e)

  def __str__(self):
    return f"*{self.expr}"

class AssignExpr(Expr):
  # Represents assignment.
  def __init__(self, e1, e2):
    Expr.__init__(self)
    self.lhs = expr(e1)
    self.rhs = expr(e2)

  def __str__(self):
    return f"{self.lhs} = {self.rhs}"

def expr(x):
  # Turn a Python object into an expression. This is solely
  # used to make simplify the writing expressions.
  if type(x) is bool:
    return BoolExpr(x)
  if type(x) is int:
    return IntExpr(x)
  if type(x) is str:
    return IdExpr(x)
  return x

def decl(x):
  # Turn a python object into a declaration.
  if type(x) is str:
    return VarDecl(x)
  return x

from lookup import resolve
from check import check
from subst import subst
from reduce import step, reduce
from evaluate import evaluate
