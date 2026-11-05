
import re


# Parse a predicate into its name and arguments
def parse_literal(literal):
    match_obj = re.match(r"^(\w+)\((.*?)\)$", literal.strip())

    if match_obj:
        predicate = match_obj.group(1)
        arguments = match_obj.group(2).split(",")
        arguments = [arg.strip() for arg in arguments]
        return predicate, arguments

    return literal.strip(), None


# Check whether an argument is a variable
# Variables must start with an uppercase letter
def is_variable(term):
    return term[0].isupper()


# Unification function
def unify(pattern, fact, substitution):

    p_pred, p_args = parse_literal(pattern)
    f_pred, f_args = parse_literal(fact)

    # Predicate names must match
    if p_pred != f_pred:
        return None

    # Handle predicates without arguments
    if p_args is None or f_args is None:
        if pattern == fact:
            return substitution.copy()
        return None

    # Number of arguments must match
    if len(p_args) != len(f_args):
        return None

    new_substitution = substitution.copy()

    for p_arg, f_arg in zip(p_args, f_args):

        # Variable matching
        if is_variable(p_arg):

            if p_arg in new_substitution:
                if new_substitution[p_arg] != f_arg:
                    return None
            else:
                new_substitution[p_arg] = f_arg

        # Constant matching
        elif p_arg != f_arg:
            return None

    return new_substitution


# Find all substitutions satisfying all premises
def find_substitutions(premises, facts, index=0, substitution=None):

    if substitution is None:
        substitution = {}

    # All premises successfully matched
    if index == len(premises):
        return [substitution]

    results = []

    current_premise = premises[index]

    for fact in facts:

        new_substitution = unify(
            current_premise,
            fact,
            substitution
        )

        if new_substitution is not None:

            results.extend(
                find_substitutions(
                    premises,
                    facts,
                    index + 1,
                    new_substitution
                )
            )

    return results


# Substitute variables in a conclusion
def substitute(expression, substitution):

    predicate, arguments = parse_literal(expression)

    if arguments is None:
        return expression

    new_arguments = []

    for arg in arguments:
        new_arguments.append(
            substitution.get(arg, arg)
        )

    return predicate + "(" + ",".join(new_arguments) + ")"


# FOL Forward Chaining Algorithm
def fol_forward_chaining(KB, query):

    # Check whether query already exists
    for fact in KB["facts"]:
        if unify(query, fact, {}) is not None:
            return True

    # Repeat until no new facts are generated
    while True:

        new_facts = set()

        # Check every rule in the Knowledge Base
        for rule in KB["rules"]:

            premises = rule[0]
            conclusion = rule[1]

            # Find substitutions satisfying all premises
            substitutions = find_substitutions(
                premises,
                KB["facts"]
            )

            for substitution in substitutions:

                # Infer a new fact
                inferred = substitute(
                    conclusion,
                    substitution
                )

                # Check whether the inferred fact proves query
                if unify(query, inferred, {}) is not None:
                    return True

                # Store only facts not already in KB
                if inferred not in KB["facts"]:
                    new_facts.add(inferred)

        # Stop if no new facts can be inferred
        if not new_facts:
            return False

        # Add newly inferred facts to Knowledge Base
        KB["facts"].update(new_facts)


# Function to display the result
def execute_test(KB, query):

    result = fol_forward_chaining(KB, query)

    if result:
        print("Query proved successfully!")
        print("Result: TRUE")
    else:
        print("Query could not be proved.")
        print("Result: FALSE")


# -------------------------------------------------
# TEST CASE 1: Human -> Mortal
# -------------------------------------------------

print("\nTEST CASE 1")

KB = {
    "facts": {
        "Human(Socrates)"
    },

    "rules": [
        (
            ["Human(X)"],
            "Mortal(X)"
        )
    ]
}

query = "Mortal(Socrates)"

execute_test(KB, query)


# -------------------------------------------------
# TEST CASE 2: Cat -> Feline -> Animal
# -------------------------------------------------

print("\nTEST CASE 2")

KB1 = {
    "facts": {
        "cat(simba)"
    },

    "rules": [
        (
            ["cat(X)"],
            "feline(X)"
        ),

        (
            ["feline(X)"],
            "animal(X)"
        )
    ]
}

query1 = "animal(simba)"

execute_test(KB1, query1)


# -------------------------------------------------
# TEST CASE 3: Brass -> Yellowmetal -> Goldlookalike
# -------------------------------------------------

print("\nTEST CASE 3")

KB2 = {
    "facts": {
        "brass(coin)"
    },

    "rules": [
        (
            ["brass(Y)"],
            "yellowmetal(Y)"
        ),

        (
            ["yellowmetal(Y)"],
            "goldlookalike(Y)"
        )
    ]
}

query2 = "goldlookalike(coin)"

execute_test(KB2, query2)


# -------------------------------------------------
# TEST CASE 4: Multiple Premises
# -------------------------------------------------

print("\nTEST CASE 4")

KB3 = {
    "facts": {
        "lion(leo)"
        # hungry(leo) is missing
    },

    "rules": [
        (
            ["lion(X)", "hungry(X)"],
            "dangerous(X)"
        )
    ]
}

query3 = "dangerous(leo)"

execute_test(KB3, query3)


# -------------------------------------------------
# TEST CASE 5: No Matching Rule
# -------------------------------------------------

print("\nTEST CASE 5")

KB4 = {
    "facts": {
        "blue(sky)"
    },

    "rules": [
        (
            ["green(Z)"],
            "plant(Z)"
        )
    ]
}

query4 = "plant(sky)"

execute_test(KB4, query4)


# -------------------------------------------------
# TEST CASE 6: Multiple Premises with Different Facts
# -------------------------------------------------

print("\nTEST CASE 6")

KB5 = {
    "facts": {
        "lion(leo)",
        "hungry(leo)"
    },

    "rules": [
        (
            ["lion(X)", "hungry(X)"],
            "dangerous(X)"
        )
    ]
}

query5 = "dangerous(leo)"

execute_test(KB5, query5)
