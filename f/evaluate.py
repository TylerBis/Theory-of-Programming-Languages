from lang import *
from decorate import *

import copy

clone = copy.deepcopy

# This module implements implements big-step semantics.
#
# In particular, it implements the relation S |- e | s => v | s' where
# e is an expression, v is value (see below), S is call stack and s is 
# the dynamic store (heap). Note that => is my approximation of the 
# usual down arrow relation used in the TAPL book.
#
# The stack S is a list of bindings from names to values. The heap
# is a list of addresses with stored values. For simplicity, the
# heap simply collects all allocations and never deletes them.
#
# There is one main function: evaluate, which computes the 
# value of an expression. A value is a Python object.

class Closure:
  # Represents the value of a lambda abstraction. This combines
  # the abstraction and an environment, which provides values
  # during application.
  def __init__(self, abs, env):
    self.abs = abs
    self.env = clone(env)

  def __str__(self):
    # TODO: Write out closed environment?
    return f"<{str(self.abs)}>"

class Location:
  # A location in the heap. This is simply its index in the heap.
  def __init__(self, ix):
    self.index = ix

  def __str__(self):
    return f"@{self.index}"

class Tuple:
  # A tuple value. A tuple is simply a list of values.
  def __init__(self, vs : list):
    self.values = vs

  def __str__(self):
    vs = ",".join([str(v) for v in self.values])
    return f"{{{vs}}}"

class Field:
  # A field maps an identifier to its value.
  def __init__(self, n, v):
    self.id = n
    self.value = v

  def __str__(self):
    return f"{self.id}={self.value}"

class Record:
  # A record value. This is a list of fields.
  def __init__(self, fs : list):
    # This list of fields
    self.fields = fs

    # A mapping of FieldDecl objects to values. This supports
    # reasonably efficient value lookup for evaluation.
    #
    # If we reduced member references to indexes, we could
    # simply extract the value from the field list, like
    # we do with tuples.
    self.select = {f.id:f.value for f in fs}

  def __str__(self):
    fs = ",".join([str(e) for e in self.fields])
    return f"{{{fs}}}"

class Variant:
  # A variant value. This is a label and its value.
  #
  # TODO: We could have reduced the the label to an integer value
  # corresponding to the labels position in its type. I believe
  # that the width and depth subtyping rules would continue to
  # apply in those cases (i.e., indexes of restricted variants
  # would be valid in larger variants).
  def __init__(self, l, v):
    self.tag = l
    self.value = v

  def __str__(self):
    return f"<{self.tag}={self.value}>"

@checked
def eval_binary(e : Expr, stack : dict, heap : list, fn : object):
  # S |- e1|s => v1|s'   S |- e2|s' => v2|s''
  # ----------------------------------------- E-Binary-@
  #       S |- e1 @ e2|s => v1 @ v2|s''
  #
  # Operands are inherently evaluated left to right.
  v1 = evaluate(e.lhs, stack, heap)
  v2 = evaluate(e.rhs, stack, heap)
  return fn(v1, v2)

@checked
def eval_unary(e : Expr, stack : dict, heap : list, fn : object):
  #  S |- e1|s => v1|s'
  # -------------------- E-Unary-@
  # S |- @e1|s => @ v1|s
  #
  # Operands are inherently evaluated left to right.
  v1 = evaluate(e.lhs, stack, heap)
  return fn(v1)

@checked
def eval_bool(e : Expr, stack : dict, heap : list):
  # --------------------- E-True
  # S |- true|s => True|s
  #
  # ----------------------- E-False
  # S |- false|s => False|s
  return e.value

@checked
def eval_and(e : Expr, stack : dict, heap : list):
  # NOTE: This is not short-circuiting.
  return eval_binary(e, stack, heap, lambda v1, v2: v1 and v2)

@checked
def eval_or(e : Expr, stack : dict, heap : list):
  # NOTE: This is not short-circuiting.
  return eval_binary(e, stack, heap, lambda v1, v2: v1 or v2)

@checked
def eval_not(e : Expr, stack : dict, heap : list):
  return eval_unary(e, stack, heap, lambda v1: not v1)

def eval_cond(e, stack, heap : list):
  # S |- e1|s => true|s'   S |- e2|s' => v2|s''
  #-------------------------------------------- E-If-True
  #         S |- e1 ? e2 : e3|s => v2|s''
  #
  # S |- e1|s => false|s'   S |- e3|s' => v3|s''
  #--------------------------------------------- E-If-True
  #         S |- e1 ? e2 : e3|s => v3|s3''
  if evaluate(e.cond):
    return evaluate(e.true);
  else:
    return evaluate(e.false);

@checked
def eval_int(e : Expr, stack : dict, heap : list):
  # -------------------- E-Int
  # S |- n|s => int(n)|s
  return e.value

@checked
def eval_add(e : Expr, stack : dict, heap : list):
  return eval_binary(e, stack, heap, lambda v1, v2: v1 + v2)

@checked
def eval_sub(e : Expr, stack : dict, heap : list):
  return eval_binary(e, stack, heap, lambda v1, v2: v1 - v2)

@checked
def eval_mul(e : Expr, stack : dict, heap : list):
  return eval_binary(e, stack, heap, lambda v1, v2: v1 * v2)

@checked
def eval_div(e : Expr, stack : dict, heap : list):
  return eval_binary(e, stack, heap, lambda v1, v2: v1 / v2)

@checked
def eval_rem(e : Expr, stack : dict, heap : list):
  return eval_binary(e, stack, heap, lambda v1, v2: v1 % v2)

@checked
def eval_neg(e : Expr, stack : dict, heap : list):
  return eval_binary(e, stack, heap, lambda v1: -v1)

@checked
def eval_eq(e : Expr, stack : dict, heap : list):
  return eval_binary(e, stack, heap, lambda v1, v2: v1 == v2)

@checked
def eval_ne(e : Expr, stack : dict, heap : list):
  return eval_binary(e, stack, heap, lambda v1, v2: v1 != v2)

@checked
def eval_lt(e : Expr, stack : dict, heap : list):
  return eval_binary(e, stack, heap, lambda v1, v2: v1 < v2)

@checked
def eval_gt(e : Expr, stack : dict, heap : list):
  return eval_binary(e, stack, heap, lambda v1, v2: v1 > v2)

@checked
def eval_le(e : Expr, stack : dict, heap : list):
  return eval_binary(e, stack, heap, lambda v1, v2: v1 <= v2)

@checked
def eval_ge(e : Expr, stack : dict, heap : list):
  return eval_binary(e, stack, heap, lambda v1, v2: v1 >= v2)

@checked
def eval_id(e : Expr, stack : dict, heap : list):
  #    x1=v1 in S
  # ---------------- E-Id
  # S |- x|s => v1|s
  return stack[e.ref]

@checked
def eval_lambda(e : Expr, stack : dict, heap : list):
  # ------------------------------ E-Lambda
  # S |- \(xi).e|s => <\(x1i).e,S>
  #
  # This produces a closure, which is a snapshot of all objects
  # in the stack. This is *wildly* inefficient. We should only
  # compute the capture of the variables in e whose binding depth
  # is less than e (i.e., parameters declared outside of e).
  return Closure(e, stack)

def eval_call(e : Expr, stack : dict, heap : list):
  # Evaluate a call expression.
  #
  # S |- e0|s => \(xi).e1|s'   S |- ei|s'i => vi|s'i   S, si=vi |- e1|s'i => v1|s''i
  # -------------------------------------------------------------------------------- E-Call
  #                        S |- e0 (ei)|s => v0|s''i
  #
  # The arguments are evaluated and then their bindings added to the
  # stack prior to execution.
  c = evaluate(e.fn, stack, heap)
  
  if type(c) is not Closure:
    raise Exception("cannot apply a non-closure to an argument")

  # Evaluate arguments
  args = []
  for a in e.args:
    args += [evaluate(a, stack, heap)]

  # Build the new environment containing the argument mapping.
  #
  # FIXME: This seems wrong. We should be appending the closure to
  # the current stack and then evaluating. That also seems a little
  # bit wrong... If the closure has variables with the same name as
  # values on the stack, we end up overwriting them.
  env = clone(c.env)
  for i in range(len(args)):
    env[c.abs.vars[i]] = args[i]

  return evaluate(c.abs.expr, env, heap)

@checked
def eval_new(e : Expr, stack : dict, heap : list):
  # S |- e1|s => v1|s'   l1 = fresh
  # ------------------------------- E-New
  # S |- new e1|s => l1|[l1->v1]s
  v1 = evaluate(e.expr, stack, heap)
  l1 = Location(len(heap))
  heap += [v1]
  return l1

@checked
def eval_deref(e : Expr, stack : dict, heap : list):
  # S |- e1|s => l1|s'    l1=v1 in s'
  # --------------------------------- E-Deref
  #       S |- *e1|s => v1|s'
  #
  # Note that we'll get an out-of-bounds error if the index is invalid.
  l1 = evaluate(e.expr, stack, heap)
  if type(l1) is not Location:
    raise Exception("invalid reference")
  return heap[l1.index]

@checked
def eval_assign(e : Expr, stack : dict, heap : list):
  # S |- e2|s => v2|s   S |- e1|s' => l1|s''
  # ---------------------------------------- E-Deref
  #    S |- e1 = e2|s => l1|[l1->v2]s''
  #
  # Operands are evaluated right to left. The effect is to update
  # location of e1 to the value of e2.
  v2 = evaluate(e.rhs, stack, heap)
  l1 = evaluate(e.lhs, stack, heap)
  if type(l1) is not Location:
    raise Exception("invalid reference")
  heap[l1.index] = v2

@checked
def eval_tuple(e : Expr, stack : dict, heap : list):
  # FIXME: Document semantics.
  vs = []
  for x in e.elems:
    vs += [evaluate(x, stack, heap)]
  return Tuple(vs)

def eval_proj(e : Expr, stack : dict, heap : list):
  # FIXME: Document semantics.
  v1 = evaluate(e.obj, stack, heap)
  return v1.values[e.index]

def eval_record(e : Expr, stack : dict, heap : list):
  # FIXME: Document semantics.
  fs = []
  for f in e.fields:
    fs += [Field(f.id, evaluate(f.value, stack, heap))]
  return Record(fs)

def eval_member(e : Expr, stack : dict, heap : list):
  # FIXME: Document semantics.
  v1 = evaluate(e.obj, stack, heap)
  return v1.select[e.id]

def eval_variant(e : Expr, stack : dict, heap : list):
  v1 = evaluate(e.field.value)
  return Variant(e.field.id, v1)

def eval_case(e : Expr, stack : dict, heap : list):
  v1 = evaluate(e.expr, stack, heap)

  # Search for the corresponding label.
  #
  # This could be more efficient if we produced a mapping from
  # labels to cases.
  case = None
  for c in e.cases:
    if c.id == v1.tag:
      case = c
      break
  assert case != None

  # Execute the case as if calling a function.
  env = clone(stack)
  env[c.var] = v1.value
  return evaluate(c.expr, env, heap)


def evaluate(e : Expr, stack : dict = {}, heap = []):
  # Evaluate an expression. The stack is the calls stack.

  # Boolean expressions

  if type(e) is BoolExpr:
    return eval_bool(e, stack, heap)

  if type(e) is AndExpr:
    return eval_and(e, stack, heap)

  if type(e) is OrExpr:
    return eval_or(e, stack, heap)

  if type(e) is NotExpr:
    return eval_not(e, stack, heap)

  if type(e) is IfExpr:
    return eval_if(e, stack, heap)

  # Arithmetic expressions

  if type(e) is IntExpr:
    return eval_int(e, stack, heap)

  if type(e) is AddExpr:
    return eval_add(e, stack, heap)

  if type(e) is SubExpr:
    return eval_sub(e, stack, heap)

  if type(e) is MulExpr:
    return eval_mul(e, stack, heap)

  if type(e) is DivExpr:
    return eval_div(e, stack, heap)

  if type(e) is RemExpr:
    return eval_rem(e, stack, heap)

  if type(e) is NegExpr:
    return eval_neg(e, stack, heap)

  # Relational expressions

  if type(e) is EqExpr:
    return eval_eq(e, stack, heap)

  if type(e) is NeExpr:
    return eval_ne(e, stack, heap)

  if type(e) is LtExpr:
    return eval_lt(e, stack, heap)

  if type(e) is GtExpr:
    return eval_gt(e, stack, heap)

  if type(e) is LeExpr:
    return eval_le(e, stack, heap)

  if type(e) is GeExpr:
    return eval_ge(e, stack, heap)

  # Functional expressions

  if type(e) is LambdaExpr:
    return eval_lambda(e, stack, heap)

  if type(e) is CallExpr:
    return eval_call(e, stack, heap)

  # Reference expressions

  if type(e) is NewExpr:
    return eval_new(e, stack, heap)

  if type(e) is DerefExpr:
    return eval_deref(e, stack, heap)

  if type(e) is AssignExpr:
    return eval_assign(e, stack, heap)

  # Data expressions

  if type(e) is TupleExpr:
    return eval_tuple(e, stack, heap)

  if type(e) is ProjExpr:
    return eval_proj(e, stack, heap)

  if type(e) is RecordExpr:
    return eval_record(e, stack, heap)

  if type(e) is MemberExpr:
    return eval_member(e, stack, heap)

  if type(e) is VariantExpr:
    return eval_variant(e, stack, heap)

  if type(e) is CaseExpr:
    return eval_case(e, stack, heap)

  assert False
