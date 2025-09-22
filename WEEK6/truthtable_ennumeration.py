import itertools
import pandas as pd
from tabulate import tabulate
import re

# Helper: convert booleans to T/F
def tf(val):
    return "T" if val else "F"

# Replace logical symbols (∨, ∧, ¬) with Python equivalents
def translate(expr: str) -> str:
    return (
        expr.replace("∨", " or ")
            .replace("∧", " and ")
            .replace("¬", " not ")
    )

# === Take KB and α (query) from user ===
kb_expr = input("Enter your Knowledge Base (use ∧, ∨, ¬): ")
alpha_expr = input("Enter your α (query) (use ∧, ∨, ¬): ")

# Translate to Python syntax
kb_py = translate(kb_expr)
alpha_py = translate(alpha_expr)

# === Detect variables dynamically (any single letter, uppercase/lowercase) ===
vars_in_expr = sorted(set(re.findall(r"\b[a-zA-Z]\b", kb_expr + alpha_expr)))

if not vars_in_expr:
    raise ValueError("No variables detected. Please use single letters like A, b, C...")

# Generate truth table
rows = []
for values in itertools.product([False, True], repeat=len(vars_in_expr)):
    local_vars = dict(zip(vars_in_expr, values))
    kb_val = eval(kb_py, {}, local_vars)
    alpha_val = eval(alpha_py, {}, local_vars)

    row = {var: tf(val) for var, val in local_vars.items()}
    row["KB"] = tf(kb_val)
    row[f"α = {alpha_expr}"] = tf(alpha_val)
    rows.append(row)

# Convert to DataFrame
df = pd.DataFrame(rows)

# Full truth table
print("\n=== Full Truth Table ===")
print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))

# Filtered truth table (only KB = T)
filtered_df = df[df["KB"] == "T"]

print("\n=== Rows where KB is True ===")
if not filtered_df.empty:
    print(tabulate(filtered_df, headers="keys", tablefmt="fancy_grid", showindex=False))
else:
    print("No rows where KB is True (KB is unsatisfiable).")

# Entailment check
query_col = f"α = {alpha_expr}"
entails = all(filtered_df[query_col] == "T") if not filtered_df.empty else True
print(f"\nDoes KB entail α ({alpha_expr})? ->", "Yes" if entails else "No")
print("Sanchit Mehta - 1BM23CS299\n")
