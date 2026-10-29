from itertools import product


# Logical implication: P -> Q
def implies(P, Q):
    return (not P) or Q


# Knowledge Base:
# KB = (Q -> P) AND (P -> NOT Q) AND (Q OR R)
def evaluate_kb(P, Q, R):
    return (
        implies(Q, P)
        and implies(P, not Q)
        and (Q or R)
    )


# Evaluate the query
# 1: R
# 2: R -> P
# 3: Q -> R
def evaluate_query(choice, P, Q, R):
    if choice == 1:
        return R
    elif choice == 2:
        return implies(R, P)
    elif choice == 3:
        return implies(Q, R)


# Truth-table enumeration algorithm
def entails(choice):
    # Generate all 2^3 = 8 truth assignments
    for P, Q, R in product([False, True], repeat=3):

        kb = evaluate_kb(P, Q, R)
        query = evaluate_query(choice, P, Q, R)

        # Counterexample: KB is true, but query is false
        if kb and not query:
            return False

    # No counterexample found
    return True


# Display the complete truth table including query columns
def print_truth_table():
    print("TRUTH TABLE ENUMERATION\n")

    print("P Q R | Q->P P->!Q Q|R | KB  | Q1:R Q2:R->P Q3:Q->R")
    print("----------------------------------------------------")

    for P, Q, R in product([False, True], repeat=3):

        first = implies(Q, P)
        second = implies(P, not Q)
        third = Q or R
        kb = evaluate_kb(P, Q, R)

        # Query values
        q1 = evaluate_query(1, P, Q, R)
        q2 = evaluate_query(2, P, Q, R)
        q3 = evaluate_query(3, P, Q, R)

        # Convert Boolean values to T/F
        tf = lambda x: "T" if x else "F"

        print(
            f"{tf(P)} {tf(Q)} {tf(R)} |"
            f"   {tf(first)}    {tf(second)}    "
            f"{tf(third)} | {tf(kb)}  |"
            f"   {tf(q1)}     {tf(q2)}      {tf(q3)}"
        )


# Print models where KB is True
def print_kb_models():
    print("\nKNOWLEDGE BASE (KB) ANALYSIS")
    print("KB Formula: (Q -> P) AND (P -> ~Q) AND (Q OR R)")
    print("KB is True under the following models (assignments):")

    true_kb_rows = []
    for P, Q, R in product([False, True], repeat=3):
        if evaluate_kb(P, Q, R):
            true_kb_rows.append((P, Q, R))

    for idx, (P, Q, R) in enumerate(true_kb_rows, 1):
        print(f"{idx}. P={P}, Q={Q}, R={R}")


# Main program
print_truth_table()
print_kb_models()

print("\nENTAILMENT RESULTS")

queries = {
    1: "R",
    2: "(R -> P)",
    3: "(Q -> R)"
}

for choice, query in queries.items():
    result = entails(choice)
    answer = "YES" if result else "NO"

    print(f"KB entails {query}: {answer}")