from lang import *
from decorate import *

@checked
def lookup(id : str, scope : list):
  # Perform name lookup. Search the scope stack for the first
  # declaration of `id`. Returns the declaration or None if 
  # the name is undeclared.
  for scope in reversed(scope):
    if id in scope:
      return scope[id]
  return None

@checked
def resolve_unary_expr(e : Expr, scope : list):
  resolve_expr(e.expr, scope)
  return e

@checked
def resolve_binary_expr(e : Expr, scope : list):
  resolve_expr(e.lhs, scope)
  resolve_expr(e.rhs, scope)
  return e

def resolve_exprs(es, scope):
  # Resolve each expression in es.
  for e in es:
    resolve_expr(e, scope)

@checked
def resolve_expr(e : Expr, scope : list):
  # Resolve references to declared variables. This requires a scope
  # stack. A scope is a mappings from names to their declarations.
  #
  # Returns the modified (in-place) tree.

  # Boolean expressions

  if type(e) is BoolExpr:
    return e

  if type(e) is AndExpr:
    return resolve_binary_expr(e, scope)

  if type(e) is OrExpr:
    return resolve_binary_expr(e, scope)

  if type(e) is NotExpr:
    return resolve_unary_expr(e, scope)

  if type(e) is IfExpr:
    resolve_expr(e.cond, scope)
    resolve_expr(e.true, scope)
    resolve_expr(e.false, scope)
    return e

  # Arithmetic expressions

  if type(e) is IntExpr:
    return e

  if type(e) is AddExpr:
    return resolve_binary_expr(e, scope)

  if type(e) is SubExpr:
    return resolve_binary_expr(e, scope)

  if type(e) is MulExpr:
    return resolve_binary_expr(e, scope)

  if type(e) is DivExpr:
    return resolve_binary_expr(e, scope)

  if type(e) is RemExpr:
    return resolve_binary_expr(e, scope)

  if type(e) is NegExpr:
    return resolve_unary_expr(e, scope)

  # Relational expressions

  if type(e) is EqExpr:
    return resolve_binary_expr(e, scope)

  if type(e) is NeExpr:
    return resolve_binary_expr(e, scope)

  if type(e) is LtExpr:
    return resolve_binary_expr(e, scope)

  if type(e) is GtExpr:
    return resolve_binary_expr(e, scope)

  if type(e) is LeExpr:
    return resolve_binary_expr(e, scope)

  if type(e) is GeExpr:
    return resolve_binary_expr(e, scope)

  # Lambda expressions

  if type(e) is IdExpr:
    # Perform name lookup.
    d = lookup(e.id, scope)
    if not d:
      raise Exception("name lookup error")
    if type(d) is not VarDecl:
      raise Exception(f"'{str(d)}' does not declare a value")

    # Bind the expression to its declaration.
    e.ref = d
    return e

  if type(e) is LambdaExpr:
    # Because of generics, we have to resolve parameter types.
    for v in e.vars:
      resolve_type(v.type, scope)

    # Create a new stack for resolving parameters.
    new = scope + [{var.id:var for var in e.vars}]
    resolve_expr(e.expr, new)
    return e

  if type(e) is CallExpr:
    resolve_expr(e.fn, scope)
    resolve_exprs(e.args, scope)
    return e

  # Reference expressions

  if type(e) is NewExpr:
    return resolve_unary_expr(e, scope)

  if type(e) is DerefExpr:
    return resolve_unary_expr(e, scope)

  if type(e) is AssignExpr:
    return resolve_binary_expr(e, scope)

  # Data expressions

  if type(e) is TupleExpr:
    resolve_exprs(e.elems, scope)
    return e

  if type(e) is ProjExpr:
    # We can't check the validity of the index because
    # we don't haver the type of the object, only the
    # expression that computes the tuple.
    resolve_expr(e.obj)
    return e

  if type(e) is RecordExpr:
    for f in e.fields:
      resolve_expr(f.value)
    return e

  if type(e) is MemberExpr:
    # We can't check the validity of the index because
    # we don't haver the type of the object, only the
    # expression that computes the tuple.
    resolve_expr(e.obj)
    return e

  if type(e) is VariantExpr:
    # We could hypothetically check the label against the
    # type, but we'll defer until typing so that all of
    # these operations are done at the same time.
    resolve_expr(e.field.value)
    return e

  if type(e) is CaseExpr:
    resolve(e.expr)
    for c in e.cases:
      new = scope + [{c.var.id, c.var}]
      resolve_expr(c.expr, new)
    return e

  if type(e) is GenericExpr:
    # Push type variables and resolve expression.
    new = scope + [{var.id:var for var in e.vars}]
    resolve_expr(e.expr, new)
    return e

  if type(e) is InstExpr:
    resolve_expr(e.gen, scope)
    resolve_types(e.args, scope)
    return e

  print(repr(e))
  assert False

def resolve_types(ts, scope):
  # Recursively resolve a list of types.
  for t in ts:
    resolve(t, scope)

def resolve_type(t : Type, scope : list = []):
  # Lookup and resolve id types in t.

  # Fundamental types

  if type(t) is BoolType:
    return t

  if type(t) is IntType:
    return t

  # Functional types

  if type(t) is FnType:
    resolve_types(t.parms, scope)
    resolve_type(t.ret, scope)
    return t

  # Reference types

  if type(t) is RefType:
    resolve_type(t.ref, scope)
    return t

  # Data types

  if type(t) is TupleType:
    resolve_types(t.elems, scope)
    return t

  if type(t) is RecordType:
    for f in t.fields:
      resolve(f.type, scope)
    return t

  if type(t) is VariantType:
    for f in t.fields:
      resolve(f.type, scope)
    return t

  # Polymorphic types

  if type(t) is IdType:
    # Perform name lookup.
    d = lookup(t.id, scope)
    if not d:
      raise Exception("name lookup error")
    if type(d) is not TypeDecl:
      raise Exception(f"'{str(d)}' does not declare a type")

    # Bind the expression to its declaration.
    t.ref = d
    return t

  if type(t) is UniversalType:
    # Push a new lexical scope for type variables.
    new = scope + [{p.id:p for p in t.parms}]
    resolve(t.type, new)
    return t

  if type(t) is ExistentialType:
    # Push a new lexical scope for type variables.
    new = scope + [{p.id:p for p in t.parms}]
    resolve(t.type, new)
    return t

  print(repr(t))
  assert False

def resolve(x, scope = []):
  if isinstance(x, Expr):
    return resolve_expr(x, scope)
  if isinstance(x, Type):
    return resolve_type(x, scope)
  print(repr(x))
  assert False
