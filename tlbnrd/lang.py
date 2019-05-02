

class VarDecl:
  # Represents the declaration of a variable declaration.
  # 
  # Note that this is NOT an expression. It is the declaration 
  # of a name.
  def __init__(self, id, t):
    self.id = id
    self.type = typify(t)

  def __str__(self):
    return f"{self.id}:{str(self.type)}"

class FieldDecl:
  # Like a VarDecl, but for fields and variants.
  def __init__(self, id, t):
    self.id = id
    self.type = typify(t)

  def __str__(self):
    return f"{self.id}:{str(self.type)}"

class FieldInit:
  # Represents the explicit initialization of (certain) variables
  # with a value.
  def __init__(self, id, e):
    self.id = id
    self.value = expr(e)

  def __str__(self):
    return f"{self.id}={str(self.value)}"

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
    self.parms = list(map(typify, parms))
    self.ret = typify(ret)

  def __str__(self):
    parms = ",".join([str(p) for p in self.parms])
    return f"({parms})->{str(self.ret)}"

class RefType(Type):
  # Represents types of the form 'Ref T1'.
  def __init__(self, t):
    self.ref = typify(t)

  def __str__(self):
    return f"Ref {str(self.ref)}"

class TupleType(Type):
  # Represents types of the form '{T1, ..., Tn}'
  def __init__(self, ts):
    self.elems = list(map(typify, ts))

  def __str__(self):
    es = ",".join([str(t) for t in self.elems])
    return f"{{{es}}}"

class RecordType(Type):
  # Represents types of the form '{li:T1, ..., xn:Tn}'
  def __init__(self, fs):
    self.fields = list(map(field, fs))

  def __str__(self):
    fs = ",".join(str(f) for f in self.fields)
    return f"{{{fs}}}"

class VariantType(Type):
  # Represents types of the form '<li:T1, ..., xn:Tn>'
  def __init__(self, fs):
    self.fields = list(map(field, fs))

  def __str__(self):
    fs = ",".join(str(f) for f in self.fields)
    return f"<{fs}>"

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
  #         D -- data expressions
  #
  #   B ::= true
  #         false
  #         e1 and e2
  #         e1 or e2
  #         not e1
  #         e1 ? e2 : e3
  #
  #   Z ::= n
  #         e1 + e2
  #         e1 - e2
  #         e1 * e2
  #         e1 / e2
  #         e1 % e2
  #         -e1
  #         e1 == e2
  #         e1 != e2
  #         e1 < e2
  #         e1 > e2
  #         e1 <= e2
  #         e1 >= e2
  #
  #   L ::= x
  #         \(x1:T1, ..., xn:Tn).e1
  #         e0(e1, e2, ..., en)
  #
  #   R ::= new e1
  #         *e1
  #         e1 = e2
  #
  #   D ::= {e1, ..., en}
  #         e1.n
  #         {x1=e1, ..., xn=en}
  #         e1.x
  #         <x1=e> as T
  #         case e1 of <xi=li> => ei
  
  def __init__(self):
    self.type = None

## Boolean expressions

class BoolExpr(Expr):
  # Represents the literals 'true' and 'false'.
  def __init__(self, val):
    Expr.__init__(self)
    self.value = val

  def __str__(self):
    return "true" if self.value else "false"

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

# Data expressions
class TupleExpr(Expr):
  def __init__(self, es):
    Expr.__init__(self)
    self.elems = list(map(expr, es))

  def __str__(self):
    es = ",".join(str(e) for e in self.elems)
    return f"{{{es}}}"

class ProjExpr(Expr):
  def __init__(self, e1, n):
    Expr.__init__(self)
    self.obj = e1
    self.index = n

  def __str__(self):
    return f"{str(self.obj)}.{self.index}"

class RecordExpr(Expr):
  def __init__(self, fs):
    Expr.__init__(self)
    self.fields = list(map(init, fs))

  def __str__(self):
    fs = ",".join(str(e) for e in self.fields)
    return f"{{{fs}}}"

class MemberExpr(Expr):
  def __init__(self, e1, id):
    Expr.__init__(self)
    self.obj = e1
    self.id = id

    # Binds to the corresponding field declaration, so we can
    # easily determine the type of the expression.
    self.Ref = None

  def __str__(self):
    return f"{str(self.obj)}.{self.id}"

class VariantExpr(Expr):
  # Expressions '<x1=e1> as T1'.
  def __init__(self, f, t):
    Expr.__init__(self)
    self.field = init(f)
    self.variant = typify(t)

  def __str__(self):
    return f"<{str(self.field)}> as {str(self.type)}"

class Case:
  # An individual case '<l1=x1> => e1'.
  #
  # This is similar to an untyped lambda abstraction \x1.e1. Note
  # that x1 should be typed in this language, but we can't compute
  # the type of the x1 until type checking.
  def __init__(self, id, n, e):
    self.id = id # The label l1
    self.var = VarDecl(n, None) # The untyped variable x1
    self.expr = expr(e) # The expression to evaluate
  
  def __str__(self):
    return f"<{str(self.id)}={str(self.var)}> => {str(self.expr)}"

class CaseExpr(Expr):
  # Expressions 'case e1 of <li=xi> => ei'.
  def __init__(self, e, cs):
    Expr.__init__(self)
    self.expr = expr(e)
    self.cases = list(map(case, cs))

  def __str__(self):
    cs = " | ".join([str(c) for c in self.cases])
    return f"case {str(self.expr)} of {cs}"

def typify(x):
  if x is bool:
    return BoolType()
  if x is int:
    return IntType()
  return x

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

def field(x):
  if type(x) is tuple:
    return FieldDecl(x[0], x[1])
  return x

def init(x):
  if type(x) is tuple:
    return FieldInit(x[0], x[1])
  return x

def case(x):
  if type(x) is tuple:
    return Case(x[0], x[1], x[2])
  return x

from lookup import resolve
from check import check
from subst import subst
from reduce import step, reduce
from evaluate import evaluate
