import json

def load_rules():
    with open("rules.json", "r") as f:
        return json.load(f)

def check_compliance(row, rules):
    violations = []
    for rule in rules:
        if row["category"] == rule["category"]:
            field_value = row[rule["field"]]
            expected = f"<= {rule['value']}" if rule["condition"] == "greater_than" else f">= {rule['value']}"
            if rule["condition"] == "greater_than" and field_value > rule["value"]:
                violations.append({
                    "rule_id": rule["rule_id"],
                    "description": rule["description"],
                    "field": rule["field"],
                    "value": field_value,
                    "expected": expected
                })
            elif rule["condition"] == "less_than" and field_value < rule["value"]:
                violations.append({
                    "rule_id": rule["rule_id"],
                    "description": rule["description"],
                    "field": rule["field"],
                    "value": field_value,
                    "expected": expected
                })

    return {
        "Transaction_ID": row["transaction_id"],
        "Compliant": len(violations) == 0,
        "Violations": violations
    }
