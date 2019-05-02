from lang import *

# Implements the typing relation e : T, which
# is to say that every expression e has some type
# T. If not, the expression is ill-typed (or
# sometimes ill-formed).

# The (only) boolean type
boolType = BoolType()

# The (only) integer type
intType = IntType()

def is_bool(x):
  # Returns true if x either is boolType (when
  # x is a Type) or if x has boolType (when x
  # is an expression). The latter case will
  # recursively compute the the type of the
  # expression as a "convenience".
  if isinstance(x, Type):
    return x == boolType
  if isinstance(x, Expr):
    return is_bool(check(x))

def is_int(x):
  # Same as above, but for int.
  if isinstance(x, Type):
    return x == intType
  if isinstance(x, Expr):
    return is_int(check(x))

def is_same_type(t1, t2):
  # Returns true if t1 and t2 are the same
  # type (if both are types).

  # Quick reject. t1 and t2 are not objects
  # of the same type.
  if type(t1) is not type(t2):
    return False

  if type(t1) is BoolType:
    return True
  
  if type(t1) is IntType:
    return True

  assert False

def has_same_type(e1, e2):
  # Returns true if e1 and e2 have the
  # same type (recursively computing the
  # types of both expressions.)
  return is_same_type(check(e1), check(e2))

def check_bool(e):
  # -------- T-Bool
  # b : Bool
  return boolType

def check_int(e):
  # -------- T-Int
  # n : Int
  return intType

def check_and(e):
  # e1 : Bool   e2 : Bool
  # --------------------- T-And
  #   e1 and e2 : Bool
  if is_bool(e1) and is_bool(e2):
    return boolType
  raise Exception("invalid operands to 'and'")

def check_add(e):
  # e1 : Int   e2 : Int
  # ------------------- T-Add
  #   e1 + e2 : Int
  if is_int(e.lhs) and is_int(e.rhs):
    return intType
  raise Exception("invalid operands to '+'")

def check_sub(e):
  # e1 : Int   e2 : Int
  # ------------------- T-Sub
  #   e1 - e2 : Int
  if is_int(e.lhs) and is_int(e.rhs):
    return intType
  raise Exception("invalid operands to '-'")

def check_eq(e):
  # e1 : T1   e2 : T2
  # ----------------- T-Eq
  #   e1 == e2 : Bool
  if has_same_type(e.lhs, e.rhs):
    return boolType
  raise Exception("invalid operands to '=='")

def do_check(e):
  # Compute the type of e.
  assert isinstance(e, Expr)

  if type(e) is BoolExpr:
    return check_bool(e)

  if type(e) is AndExpr:
    return check_and(e)

  if type(e) is OrExpr:
    return check_or(e)

  if type(e) is NotExpr:
    return check_not(e)

  if type(e) is IfExpr:
    return check_if(e)

  if type(e) is IntExpr:
    return check_int(e)

  if type(e) is AddExpr:
    return check_add(e)

  if type(e) is SubExpr:
    return check_sub(e)

  if type(e) is MulExpr:
    return check_mul(e)

  if type(e) is DivExpr:
    return check_div(e)

  if type(e) is RemExpr:
    return check_rem(e)

  if type(e) is NegExpr:
    return check_neg(e)

  if type(e) is EqExpr:
    return check_eq(e)

  if type(e) is NeExpr:
    return check_ne(e)

  if type(e) is LtExpr:
    return check_lt(e)

  if type(e) is GtExpr:
    return check_gt(e)

  if type(e) is LeExpr:
    return check_le(e)

  if type(e) is GeExpr:
    return check_ge(e)

  assert False


def check(e):
  # Accepts an expression and returns its type.

  # If we've computed the type already, return it.
  if not e.type:
    e.type = do_check(e)

  return e.type



