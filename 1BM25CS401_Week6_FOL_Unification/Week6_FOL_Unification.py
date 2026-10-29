class Term:
    pass

class Variable(Term):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var({self.name})"

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Constant(Term):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Const({self.name})"

    def __eq__(self, other):
        return isinstance(other, Constant) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Function(Term):
    def __init__(self, name, args):
        self.name = name
        self.args = args # list of Terms

    def __str__(self):
        args_str = ", ".join(str(arg) for arg in self.args)
        return f"{self.name}({args_str})"

    def __repr__(self):
        return f"Func({self.name}, {repr(self.args)})"

    def __eq__(self, other):
        return isinstance(other, Function) and self.name == other.name and self.args == other.args

    def __hash__(self):
        return hash((self.name, tuple(self.args)))


def occurs_check(var, term, subst):
    """Return True if variable var occurs within term under substitution subst."""
    if var == term:
        return True
    elif isinstance(term, Variable):
        if term in subst:
            return occurs_check(var, subst[term], subst)
    elif isinstance(term, Function):
        return any(occurs_check(var, arg, subst) for arg in term.args)
    return False


def apply_subst(term, subst):
    """Apply substitution dict to a term recursively."""
    if isinstance(term, Variable):
        if term in subst:
            return apply_subst(subst[term], subst)
        return term
    elif isinstance(term, Function):
        return Function(term.name, [apply_subst(arg, subst) for arg in term.args])
    return term


def unify(x, y, subst=None):
    """Recursively find the Most General Unifier (MGU) for expressions x and y."""
    if subst is None:
        subst = {}

    # If substitution dictionary states failure
    if subst is False:
        return False

    # Apply existing substitutions first
    x = apply_subst(x, subst)
    y = apply_subst(y, subst)

    if x == y:
        return subst

    if isinstance(x, Variable):
        return unify_var(x, y, subst)

    if isinstance(y, Variable):
        return unify_var(y, x, subst)

    if isinstance(x, Function) and isinstance(y, Function):
        if x.name != y.name or len(x.args) != len(y.args):
            return False
        for arg_x, arg_y in zip(x.args, y.args):
            subst = unify(arg_x, arg_y, subst)
            if subst is False:
                return False
        return subst

    return False


def unify_var(var, val, subst):
    """Helper to unify a variable with another term."""
    if var == val:
        return subst
    if occurs_check(var, val, subst):
        print(f"Occurs check failed: {var} is inside {val}")
        return False

    # Update existing substitutions with the new one
    new_subst = {var: val}
    for v, t in subst.items():
        subst[v] = apply_subst(t, new_subst)
    subst[var] = val
    return subst


# --- TEST RUN --- 
if __name__ == "__main__":
    # Variables
    x = Variable("x")
    y = Variable("y")
    z = Variable("z")

    # Constants
    a = Constant("a")
    b = Constant("b")

    # Functions
    # term1: f(x, g(y), g(y), a)
    # term2: f(a, g(z), g(y), x)
    g_y = Function("g", [y])
    g_z = Function("g", [z])
    term1 = Function("f", [x, g_y, g_y, a])
    term2 = Function("f", [a, g_z, g_y, x])

    print(f"Unifying: {term1}  AND  {term2}")
    mgu = unify(term1, term2)
    if mgu is not False:
        print("MGU Found:")
        for var, val in mgu.items():
            print(f"  {var} -> {val}")
        
        # Apply MGU to terms to find the final expression
        final_term1 = apply_subst(term1, mgu)
        final_term2 = apply_subst(term2, mgu)
        print(f"\nFinal Unified Expression: {final_term1}")
    else:
        print("Unification Failed!")
