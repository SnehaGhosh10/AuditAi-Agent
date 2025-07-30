import json

def load_rules():
    with open("rules.json", "r") as f:
        rules = json.load(f)
    return rules

# Apply rules to each transaction
def check_compliance(transactions, rules):
    flagged = []

    for txn in transactions:
        for rule in rules:
            field = rule["field"]
            category = rule.get("category", None)
            if category and txn.get("category") != category:
                continue

            condition = rule["condition"]
            value = rule["value"]

            txn_value = txn.get(field)
            if txn_value is None:
                continue

            if condition == "greater_than" and txn_value > value:
                flagged.append({
                    "transaction": txn,
                    "rule_violation": rule["description"]
                })

    return flagged
