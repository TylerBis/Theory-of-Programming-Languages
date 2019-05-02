
# Declarations and helper classes

class VarDecl:
  # Represents the declaration of a variable declaration.
  # 
  # Note that this is NOT an expression. It is the declaration 
  # of a name.
  def __init__(self, id, t):
    self.id = id
    self.type = type_expr(t)

  def __str__(self):
    return f"{self.id}:{str(self.type)}"

class TypeDecl:
  # Represents the declaration of a type variable.
  def __init__(self, id):
    self. id = id

  def __str__(self):
    return f"{self.id}"

class FieldDecl:
  # Like a VarDecl, but for fields and variants.
  def __init__(self, id, t):
    self.id = id
    self.type = type_expr(t)

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

# Types

class Type:
  # Represents a type in the language.
  #
  # T ::= Bool
  #       Int
  #       (T1, T2, ..., Tn) -> T0
  #       Ref T1
  #       ...
  #       Dep
  pass

# Fundamental types

class BoolType(Type):
  # The type 'Bool'.
  def __init__(self):
    Type.__init__(self)

  # Represents the type 'Bool'
  def __str__(self):
    return "Bool"

class IntType(Type):
  # The type 'Int'.
  def __init__(self):
    Type.__init__(self)

  # Represents the type 'Int'
  def __str__(self):
    return "Int"

# Functional types

class FnType(Type):
  # Represents types of the form '(T1, T2, ..., Tn) -> T0'
  def __init__(self, parms, ret):
    Type.__init__(self)
    self.parms = list(map(type_expr, parms))
    self.ret = type_expr(ret)

  def __str__(self):
    parms = ",".join([str(p) for p in self.parms])
    return f"({parms})->{str(self.ret)}"

# Reference types

class RefType(Type):
  # Represents types of the form 'Ref T1'.
  def __init__(self, t):
    Type.__init__(self)
    self.ref = type_expr(t)

  def __str__(self):
    return f"Ref {str(self.ref)}"

# Data types

class TupleType(Type):
  # Represents types of the form '{T1, ..., Tn}'
  def __init__(self, ts):
    Type.__init__(self)
    self.elems = list(map(type_expr, ts))

  def __str__(self):
    es = ",".join([str(t) for t in self.elems])
    return f"{{{es}}}"

class RecordType(Type):
  # Represents types of the form '{li:T1, ..., xn:Tn}'
  def __init__(self, fs):
    Type.__init__(self)
    self.fields = list(map(field, fs))

  def __str__(self):
    fs = ",".join(str(f) for f in self.fields)
    return f"{{{fs}}}"

class VariantType(Type):
  # Represents types of the form '<li:T1, ..., xn:Tn>'
  def __init__(self, fs):
    Type.__init__(self)
    self.fields = list(map(field, fs))

  def __str__(self):
    fs = ",".join(str(f) for f in self.fields)
    return f"<{fs}>"

# Polymorphic types

class DepType(Type):
  # The type 'Dep' of type-dependent expressions.
  def __init__(self):
    Type.__init__(self)

  # Represents the type 'Dep'
  def __str__(self):
    return "Dep"

class IdType(Type):
  # Represents uses of type variables.
  #
  # This works just like IdExprs but at the type level.
  def __init__(self, x):
    Type.__init__(self)
    if type(x) is str:
      # Initialized by an unresolved string.
      self.id = x
      self.ref = None # Eventually links to a var
    elif type(x) is TypeDecl:
      # Initialized by a known variable.
      self.id = x.id
      self.ref = x

  def __str__(self):
    return f"{self.id}"

class UniversalType(Type):
  # Types of the form '\[Xi].T'. This is the type of type 
  # abstractions (i.e. GenericExprs).
  #
  # The TAPL book is a bit silent on how the types in a universal
  # type should be represented. Are they declarations or are they
  # references to the declarations? The book's use of "just strings"
  # can make it difficult to determine when a name is first
  # introduced.
  #
  # We treat them here as declarations because we can conceivably 
  # create type aliases. For example:
  #
  #   Comp = forall [T].(T, T)->Bool;
  #
  # To resolve the uses of T in the generic function type, we'd
  # to have previously declared them.
  #
  # Note that a type abstraction ALSO declares type variables:
  #
  #   min = lambda T.(a:T, b:T).a < b;
  #
  # When we check the type of the (outer) lambda, we simply reuse
  # the same parameters for the computed universal type.
  #
  # Note that T is usually (but not always?) a function type.
  #
  # TODO: Explore quantification over non-functions.
  def __init__(self, ts, t):
    Type.__init__(self)
    self.parms = list(map(type_decl, ts))
    self.type = type_expr(t)

  def __str__(self):
    ts = ",".join([str(p) for p in self.parms])
    return f"∀[{ts}].{str(self.type)}"

class ExistentialType(Type):
  # Types of the form '?[Ti].T0' where T0 is usually
  # a record type describing a set of named operations. This
  # is the type of PackExprs.
  #
  # Note that T is usually (but not always?) a record type.
  #
  # TODO: Explore quantification over non-records.
  def __init__(self, vs, t):
    Type.__init__(self)
    self.parms = list(map(type_decl, vs))
    self.type = type_expr(t)

  def __str__(self):
    ps = ",".join([str(p) for p in self.parms])
    return f"∃[{ps}].{str(self.type)}"

# The (only) boolean type
boolType = BoolType()

# The (only) integer type
intType = IntType()

# The (only) dependent type.
depType = DepType()

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
    return f"λ({parms}).{self.expr}"

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
    self.variant = type_expr(t)

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

# Polymorphic terms

class GenericExpr(Expr):
  # Terms of the form '\[ti].e'. Here, Each ti is a type variable
  # and e is an expression using those types (usually a lambda
  # expression).
  def __init__(self, vs, e):
    Expr.__init__(self)
    self.vars = list(map(type_decl, vs))
    self.expr = expr(e)

  def __str__(self):
    parms = ",".join(str(v) for v in self.vars)
    return f"λ[{parms}].{self.expr}"

class InstExpr(Expr):
  # Terms of the form 'e1 [ti]'. Represents the substitution of 
  # types into generic expressions to produce concrete expressions.
  def __init__(self, e, ts):
    Expr.__init__(self)
    self.gen = e
    self.args = list(map(type_expr, ts))

  def __str__(self):
    ts = ",".join([str(t) for t in self.args])
    return f"{str(self.gen)} [{ts}]"

class PackExpr(Expr):
  # Terms of the form '{*t1, e} as t2', which embed concrete
  # types in existential types -- in other words, this will produce
  # an existential value. The only operation on existential values
  # is unpacking them (see below).
  def __init__(self, t1, e, t2):
    Expr.__init__(self)
    self.rep = t2 # The representation type
    self.expr = e # The representation value
    self.exist = t2 # The existential type

  def __str__(self):
    return f"{{*{str(self.rep)},{str(self.expr)} as {str(self.exist)}"

class UnpackExpr(Expr):
  # Terms of the form 'let {[Xi], x}=e1 in e2'.
  #
  # Unpack expressions are kind of hard to understand in the context 
  # of the TAPL book. This operation resurfaces the types embedded
  # in the packed value in e1 so they can be used in e2.
  #
  # In the typing rules x is going to have the type of record (if it
  # is a record) of the existentially quantified type of e2, which will
  # use the types in [Xi], so we have to re-introduce those (apparently).
  def __init__(self, ts, n, e1, e2):
    Expr.__init__(self)
    self.vars = ts # Type variables appearing in the type of e1
    self.var = VarDecl(n, None) # The (not yet typed) variable x
    self.pack = e1 # The packed value
    self.expr = e2 # remaining expression

  def __str__(self):
    return f"{{*{str(self.rep)},{str(self.expr)} as {str(self.exist)}"

def type_expr(x):
  if x is bool:
    return BoolType()
  if x is int:
    return IntType()
  if type(x) is str:
    return IdType(x)
  return x

def type_decl(x):
  # Turn a python object into a declaration.
  if type(x) is str:
    return TypeDecl(x)
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
  # Turn a pair into a variable decl.
  if type(x) is tuple:
    return VarDecl(x[0], x[1])
  assert type(x) is VarDecl
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
from substitute import subst_expr, subst_type, subst
from evaluate import evaluate
from instantiate import instantiate
