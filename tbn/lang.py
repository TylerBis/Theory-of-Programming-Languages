
class Type:
  # Represents a type in the language.
  #
  # T ::= Bool | Int
  pass

class BoolType(Type):
  # Represents the type 'Bool'
  def __str__(self):
    return "Bool"

class IntType(Type):
  # Represents the type 'Int'
  def __str__(self):
    return "Int"

class Expr:
  # Represents the set of expressions in the
  # pure (or untyped) lambda calculus. This is
  # defined as:
  #
  #   e ::= b                     -- boolean literals (true and false)
  #         e1 and e2             -- logical and
  #         e1 or e2              -- logical or
  #         not e1                -- logical negation
  #         if e1 then e2 else e3 -- conditionals
  #         n                     -- integer literals
  #         e1 + e2               -- addition
  #         e1 - e2               -- subtraction
  #         e1 * e2               -- multiplication
  #         e1 / e2               -- quotient of division
  #         e1 % e2               -- remainder of division
  #         -e1                   -- negation
  #         e1 == e2              -- equality
  #         e1 != e2              -- distinction
  #         e1 < e2               -- less than
  #         e1 > e2               -- greater than
  #         e1 <= e2              -- less than or equal to
  #         e1 >= e2              -- greater than or equal to
  def __init__(self):
    # The type of the expression. This is computed 
    # by the check() function.
    self.type = None

## Boolean expressions

class BoolExpr(Expr):
  def __init__(self, val):
    Expr.__init__(self)
    self.value = val

  def __str__(self):
    return "true" if self.value else "false"

class AndExpr(Expr):
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} and {self.rhs})"

class OrExpr(Expr):
  def __init__(self, lhs, rhs):
    Expr.__init__(self)
    self.lhs = expr(lhs)
    self.rhs = expr(rhs)

  def __str__(self):
    return f"({self.lhs} or {self.rhs})"

class NotExpr(Expr):
  def __init__(self, e):
    Expr.__init__(self)
    self.expr = expr(e)

  def __str__(self):
    return f"(not {self.expr})"

class IfExpr(Expr):
  # Represents expressions of the form `if e1 then e2 else e3`.
  def __init__(self, e1, e2, e3):
    Expr.__init__(self)
    self.cond = express(e1)
    self.true = express(e2)
    self.false = express(e3)

  def __str__(self):
    return f"(if {self.cond} then {self.true} else {self.false})"

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

from reduce import reduce
from check import check
from evaluate import evaluate
