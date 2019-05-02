from lang import *
from decorate import *

# Implements the typing relation G |- e : T, which is to say that 
# every expression e has some type T. If not, the expression 
# is ill-typed (or sometimes ill-formed).
#
# For example:
#
#   \x:Int.(3 + x)
#
# x has type int in the body of the abstraction.

@checked
def is_same_type(t1 : Type, t2 : Type):
  # Returns true if t1 and t2 are the same type (if both are types).

  # Quick reject. t1 and t2 are not objects
  # of the same type.
  if type(t1) is not type(t2):
    return False

  if type(t1) is BoolType:
    return True
  
  if type(t1) is IntType:
    return True

  if type(t1) is FnType:
    for a, b in zip(t1.parms, t2.parms):
      if not is_same_type(a, b):
        return False
    return is_same_type(t1.ret, t2.ret)

  if type(t1) is RefType:
    return is_same_type(t1.ref, t2.ref)

  assert False

@checked
def is_bool(t : Type):
  # Returns true if t is Bool.
  return t == boolType;

@checked
def is_int(t : Type):
  # Returns true if t is Int.
  return t == intType;

@checked
def is_function(t : Type):
  # Returns true if t is a function type.
  return type(t) is FnType

@checked
def is_reference(t : Type):
  # Returns true if t is a reference type.
  return type(t) is RefType

@checked
def is_reference_to(t : Type, u : Type):
  # Returns true if t is a reference to u.
  return is_reference(t) and is_same_type(t.ref, u)

@checked
def is_tuple(t : Type):
  return type(t) is TupleType

@checked
def is_record(t : Type):
  return type(t) is RecordType

@checked
def is_variant(t : Type):
  return type(t) is VariantType

@checked
def has_same_type(e1 : Expr, e2 : Expr):
  # Returns true if expressions e1 and e2 have the same type.
  return is_same_type(check(e1), check(e2))

@checked
def has_bool(e : Expr):
  return is_same_type(check(e), boolType)

@checked
def has_int(e : Expr):
  # Same as above, but for int.
  return is_same_type(check(e), intType)

@checked
def check_bool(e : Expr):
  # ------------- T-Bool
  # G |- b : Bool
  return boolType

@checked
def check_int(e : Expr):
  # ------------ T-Int
  # G |- n : Int
  return intType

@checked
def check_logical_unary(e : Expr, op : str):
  #  G |- e1 : Bool
  # -----------------
  # G |- op e1 : Bool
  if is_bool(e.expr):
    return boolType

  raise Exception(f"invalid operands to '{op}'")

@checked
def check_logical_binary(e : Expr, op : str):
  # G |- e1 : Bool   G |- e2 : Bool
  # -------------------------------
  #    G |- e1 op e2 : Bool
  
  if is_bool(e.lhs) and is_bool(e.rhs):
    return boolType
  
  raise Exception(f"invalid operands to '{op}'")

@checked
def check_and(e : Expr):
  return check_logical_binary(e, "and")

@checked
def check_or(e : Expr):
  return check_logical_binary(e, "or")

@checked
def check_arithmetic_binary(e : Expr, op : str):
  # G |- e1 : Int   G |- e2 : Int
  # ----------------------------- T-Add
  #      G |- e1 op e2 : Int
  
  if is_int(e.lhs) and is_int(e.rhs):
    return intType
  
  raise Exception(f"invalid operands to '{op}'")

@checked
def check_add(e : Expr):
  return check_arithmetic_binary(e, "+")

@checked
def check_sub(e : Expr):
  return check_arithmetic_binary(e, "-")

@checked
def check_mul(e : Expr):
  return check_arithmetic_binary(e, "*")

@checked
def check_div(e : Expr):
  return check_arithmetic_binary(e, "/")

@checked
def check_rem(e : Expr):
  return check_arithmetic_binary(e, "%")

@checked
def check_relational(e : Expr, op : str):
  # G |- e1 : T1   G |- e2 : T2
  # --------------------------- T-Eq
  #    G |- e1 op e2 : Bool
  
  if has_same_type(e.lhs, e.rhs):
    return boolType
  
  raise Exception(f"invalid operands to '{op}'")  

@checked
def check_eq(e : Expr):
  return check_relational(e, "==")

@checked
def check_ne(e : Expr):
  return check_relational(e, "!=")

@checked
def check_lt(e : Expr):
  return check_relational(e, "<")

@checked
def check_gt(e : Expr):
  return check_relational(e, ">")

@checked
def check_le(e : Expr):
  return check_relational(e, "<=")

@checked
def check_ge(e : Expr):
  return check_relational(e, ">=")

@checked
def check_id(e : Expr):
  #  x : T in G
  # -----------
  # G |- x : T
  #
  # In essence, we are searching the type environment for the 
  # pair x : T. However, because we've previously bound the id
  # to its declaration, we can simply refer directly to the 
  # type of the variable.
  return e.ref.type

@checked
def check_lambda(e : Expr):
  #  G, xi:Ti :- e0 : T0
  # ---------------------
  # G |- \(xi:Ti).e0 : (Ti) -> T0
  parms = [check(p) for p in e.vars]
  ret =  check(e.expr)
  return FnType(parms, ret)

@checked
def check_call(e : Expr):
  t = check(e.fn)
  if not is_function(t):
    raise Exception("invalid function call")
  
  if len(e.args) < len(t.parms):
    raise Exception("too few arguments")
  if len(e.args) > len(t.parms):
    raise Exception("too many arguments")

  for i in range(len(e.args)):
    arg = check(e.args[i])
    parm = t.parms[i]
    if not is_same_type(arg, parm):
      raise Exception("parameter/argument mismatch")

  return t.ret

@checked
def check_new(e : Expr):
  #    G |- e1 : T1
  # --------------------
  # G |- new e1 : Ref T1
  t = check(e.expr)
  return RefType(t)

@checked
def check_deref(e : Expr):
  # G |- e1 : Ref T1
  # -----------------
  #  G |- *e1 : T1
  t = check(e.expr)
  if not is_reference(t):
    raise Exception("cannot dereference a non-reference")

  return t.ref

@checked
def check_assign(e : Expr):
  t1 = check(e.lhs)
  if not is_reference(t1):
    raise Exception("operand is not a reference")

  t2 = check(e.rhs)
  if not is_reference_to(t1, t2):
    raise Exception("type mismatch in assignment")

@checked
def check_tuple(e : Expr):
  ts = []
  for x in e.elems:
    ts += [check(x)]
  return TupleType(ts)

@checked
def check_proj(e : Expr):
  t1 = check(e.obj)
  if not is_tuple(t1):
    raise Exception("operand is not a tuple")
  if e.index < 0:
    raise Exception("negative projection index")
  if e.index >= len(t1.elems):
    raise Exception("projection index out of bounds")
  t1.elems[e.index]
  return t1.elems[e.index]

@checked
def check_record(e : Expr):
  fs = []
  for f in e.fields:
    fs += [FieldDecl(f.id, check(f.value))]
  return RecordType(fs)

@checked
def check_member(e : Expr):
  t1 = check(e.obj)
  if not is_record(t1):
    raise Exception("operand is not a tuple")
  
  # Map the id to its corresponding field decl.
  # TODO: We could build the lookup in the record type.
  fs = {f.id:f for f in t1.fields}
  if e.id not in fs:
    raise Exception("no such member")
  e.ref = fs[e.id]

  # Return the type of the computed field.
  return e.ref.type

@checked
def check_variant(e : Expr):
  t1 = check(e.field.value)

  # Check that a) there is a corresponding label
  # in the type and that b) the type of the value
  # is the same as that field.
  fs = {f.id:f for f in e.variant.fields}
  if e.field.id not in fs:
    raise Exception("no matching label in variant")
  f = fs[e.field.id]
  if not is_same_type(t1, f.type):
    raise Exception("type mismatch in variant")

  return e.variant

@checked
def check_case(e : Expr):
  t1 = check(e.expr)
  if not is_variant(t1):
    raise Exception("operand is not a variant")

  # Build a field lookup table for typing cases.
  fs = {f.id:f for f in t1.fields}

  t2 = None
  for c in e.cases:
    # Compute the variable in each case
    if c.id not in fs:
      raise Exception("no matching case label in variant")
    f = fs[c.id]
    c.var.type = f.type

    # Recursively type the expressions
    t = check(c.expr)
    if not t2:
      t2 = t
    else:
      if not is_same_type(t, t2):
        raise Exception("case type mismatch")

  return t2

@checked
def do_check(e : Expr):
  # Compute the type of e.

  # Boolean expressions
  if type(e) is BoolExpr:
    return check_bool(e)

  if type(e) is AndExpr:
    return check_logical_binary(e, "and")

  if type(e) is OrExpr:
    return check_logical_binary(e, "or")

  if type(e) is NotExpr:
    return check_logical_unary(e, "not")

  if type(e) is IfExpr:
    return check_if(e)

  # Arithmetic expressions

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

  # Relational expressions

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

  if type(e) is IdExpr:
    return check_id(e)

  # Functional expressions

  if type(e) is LambdaExpr:
    return check_lambda(e)

  if type(e) is CallExpr:
    return check_call(e)

  # Reference expressions

  if type(e) is NewExpr:
    return check_new(e)

  if type(e) is DerefExpr:
    return check_deref(e)

  if type(e) is AssignExpr:
    return check_assign(e)

  # Data expressions

  if type(e) is TupleExpr:
    return check_tuple(e)

  if type(e) is ProjExpr:
    return check_proj(e)

  if type(e) is RecordExpr:
    return check_record(e)

  if type(e) is MemberExpr:
    return check_member(e)

  if type(e) is VariantExpr:
    return check_variant(e)

  if type(e) is CaseExpr:
    return check_case(e)

  assert False

@checked
def check(e : Expr):
  # Accepts an expression and returns its type.

  # If we've computed the type already, return it.
  if not e.type:
    e.type = do_check(e)

  return e.type


