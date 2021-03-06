class Expr:
    """Implements the language:
    e ::=   T
            F
            not e1
            e1 and e2
            e1 or e2
            e1 + e2
            e1 - e2
            e1 * e2
            e1 / e2

    v ::=   T
            F
            Int
    """
    pass

# The following are for Boolean Expressions
class BoolExpr(Expr):
    """Implements a "True" or "False" statement"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"{self.value}"

class NotExpr(Expr):
    """Implements a "Not" expression:
            returns "True" if "False" or
            returns "False" if "True"
    """
    def __init__(self, expr):
        self.expr = expr
    def __str__(self):
        return f"(not {self.expr})"

class AndExpr(Expr):
    """Implements an "And" expression:
            returns lhs and rhs
    """
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def __str__(self):
        return f"({self.lhs} and {self.rhs})"

class OrExpr(Expr):
    """Implements an "Or" expression:
            returns lhs or rhs
    """
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def __str__(self):
        return f"({self.lhs} or {self.rhs})"

# Returns if expression is Boolean
def is_bool(e):
    return type(e) is BoolExpr

# Returns if expression is reducible
def is_reducible_bool(e):
    return not is_bool(e)

# Evaluate one "Not" expression
def step_not(e):
    if is_bool(e.expr):
        return BoolExpr(not e.expr.value)
    return NotExpr(step_bool(e.expr))

# Evaluate one "And" expression
def step_and(e):
    if is_bool(e.lhs) and is_bool(e.rhs):
        return BoolExpr(e.lhs.value and e.rhs.value)
    if is_reducible_bool(e.lhs):
        return AndExpr(step_bool(e.lhs), e.rhs)
    if is_reducible_bool(e.rhs):
        return AndExpr(e.lhs, step_bool(e.rhs))

# Evaluate one "Or" expression
def step_or(e):
    if is_bool(e.lhs) and is_bool(e.rhs):
        return BoolExpr(e.lhs.value or e.rhs.value)
    if is_reducible_bool(e.lhs):
        return OrExpr(step_bool(e.lhs), e.rhs)
    if is_reducible_bool(e.rhs):
        return OrExpr(e.lhs, step_bool(e.rhs))

# Evaluate one step in a Boolean expression
def step_bool(e):
    assert is_reducible_bool(e)
    if type(e) is NotExpr:
        return step_not(e)
    if type(e) is AndExpr:
        return step_and(e)
    if type(e) is OrExpr:
        return step_or(e)

# Reduces Boolean expression to either "True" or "False"
def reduce_bool(e):
    while is_reducible_bool(e):
        e = step_bool(e)
    return e

# The following are for arithmetic expressions:
class IntExpr(Expr):
    """Implements an Integer expression"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"{self.value}"

class AddExpr(Expr):
    """Implements an addition expression"""
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def __str__(self):
        return f"({self.lhs} + {self.rhs})"

class SubExpr(Expr):
    """Implements a subtraction expression"""
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def __str__(self):
        return f"({self.lhs} - {self.rhs})"

class MultExpr(Expr):
    """Implements a multiplication expression"""
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def __str__(self):
        return f"({self.lhs} * {self.rhs})"

class DivExpr(Expr):
    """Implements a division expression"""
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def __str__(self):
        return f"({self.lhs} / {self.rhs})"

# Returns "True" if expression is an Integer"
def is_int(e):
    return type(e) is IntExpr

# Returns "True" if arithmetic expression is reducible
def is_reducible_arith(e):
    return not is_int(e)

# Evaluates one addition expression
def step_add(e):
    if is_int(e.lhs) and is_int(e.rhs):
        return IntExpr(e.lhs.value + e.rhs.value)
    if is_reducible_arith(e.lhs):
        return AddExpr(step_arith(e.lhs), e.rhs)
    if is_reducible_arith(e.rhs):
        return AddExpr(e.lhs, step_arith(e.rhs))

# Evaluates one subtraction expression
def step_sub(e):
    if is_int(e.lhs) and is_int(e.rhs):
        return IntExpr(e.lhs.value - e.rhs.value)
    if is_reducible_arith(e.lhs):
        return SubExpr(step_arith(e.lhs), e.rhs)
    if is_reducible_arith(e.rhs):
        return SubExpr(e.lhs, step_arith(e.rhs))

# Evaluates one multiplication expression
def step_mult(e):
    if is_int(e.lhs) and is_int(e.rhs):
        return IntExpr(e.lhs.value * e.rhs.value)
    if is_reducible_arith(e.lhs):
        return MultExpr(step_arith(e.lhs), e.rhs)
    if is_reducible_arith(e.rhs):
        return MultExpr(e.lhs, step_arith(e.rhs))

# Evaluates one division expression
def step_div(e):
    if is_int(e.lhs) and is_int(e.rhs):
        return IntExpr(e.lhs.value / e.rhs.value)
    if is_reducible_arith(e.lhs):
        return DivExpr(step_arith(e.lhs), e.rhs)
    if is_reducible_arith(e.rhs):
        return DivExpr(e.lhs, step_arith(e.rhs))

# Evaluates one step in an arithmetic expression
def step_arith(e):
    assert is_reducible_arith(e)
    if type(e) is AddExpr:
        return step_add(e)
    if type(e) is SubExpr:
        return step_sub(e)
    if type(e) is MultExpr:
        return step_mult(e)
    if type(e) is DivExpr:
        return step_div(e)

# Evaluates arithmetic expression to an Integer 
def reduce_arith(e):
    while is_reducible_arith(e):
        e = step_arit(e)
    return (e)
