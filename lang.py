class Expr:
    """
    The language is defined by the following sets of expressions.

    e ::= true
          false
          not e1
          e1 and e2
          e1 or e2

    v ::= true
          false

    """
    pass

class BoolExpr(Expr):
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return str(self.value)

class NotExpr(Expr):
    def __init_(self, e):
        self.expr = e

    def __str__(self):
        return f"(not {self.expr})"

class AndExpr(Expr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    # def __str__(self):
    #     return f"({self.lhs} and {self.rhs})"

class OrExpr(Expr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    # def __str__(self):
    #     return f"({self.lhs} or {self.rhs})"

def same_str(e1, e2):
    return str(e1) == str(e2)

def same(e1, e2):
    # returns true when e1 and e2 the same string?
    # (or when are the not the same).

    if (type(e1) is not type(e2)):
        return False

    # What do I know about e1 and e2? They have the same type

    if type(e1) is BoolExpr:
        return e1.value == e2.value

    if type(e1) is NotExpr:
        return same(e1.expr, e2.expr)

    if type(e1) is AndExpr:
        return same(e1.lhs, e2.lhs) and same(e1.rhs, e2.rhs)

    if type(e1) is OrExpr:
        return same(e1.lhs, e2.lhs) or same(e1.rhs, e2.rhs)

def is_value(e):
    """Returns true if e is a value (i.e) irreducible)."""
    return type(e) is BoolExpr

def is_reducible(e):
    return not is_value(e)
def step_and(e):
    # ----------------------------- And-V
    # v1 and v2 -> '[v1] and [v2]'
    #
    #        e1 -> e1'
    # ----------------------------- And-L
    # e1 and e2 -> e1' and e2

    #        e2 -> e2'
    # ----------------------------- And-L
    # v1 and e2 -> v1 and e2'

    if is_value(e.lhs) and is_value(e.rhs):
        # implement the truth table
        return BoolExpr(e.lhs.value and e.rhs.value)

    if is_reducible(e.lhs):
        return AndExpr(step(e.lhs), e.rhs)

    if is_reducible(e.rhs):
        return AndExpr(e.lhs, step(e.rhs))

    assert False

def step_or(e):
    # ----------------------------- Or-V
    #   v1 or v2 -> '[v1] or [v2]'
    #
    #         e1 -> e1'
    # ----------------------------- Or-L
    #   e1 or e2 -> e1' or e2

    #         e2 -> e2'
    # ----------------------------- Or-L
    #   v1 or e2 -> v1 or e2'

    if is_value(e.lhs) and is_value(e.rhs):
        # implement the truth table
        return BoolExpr(e.lhs.value or e.rhs.value)

    if is_reducible(e.lhs): # Applies Or-L
        return OrExpr(step(e.lhs), e.rhs)

    if is_reducible(e.rhs): # Applies Or-R
        return OrExpr(e.lhs, step(e.rhs))

    assert False


def step(e):
    """Compute the next state of the program."""
    assert is_reducible(e)

    if type(e) is NotExpr:
        #------------------- Not-T
        # not true -> false
        #------------------- Not-F
        # not false -> true
        #
        # Alternative for above:
        # ------------------
        # not v1 -> 'not [v1]'
        #
        #     e1 -> e1'
        # ------------------ Not-E
        # not e1 -> not e1'

        if is_value(e.expr):
            if e.expr.value == True: # not true
                return BoolExpr(False)
            else:
                return BoolExpr(True) # not false

        return NotExpr(step(e.expr))

    if type(e) is AndExpr:
        return step_and(e)

    if type(e) is OrExpr:
        return step_or(e)

    def reduce(e):
        while is_reducible(e):
            e = step(e)
        return e
