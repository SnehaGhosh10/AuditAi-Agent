import json

def load_rules():
    with open("data/rules.json", "r") as f:
        return json.load(f)

def check_compliance(row, rules):
    issues = []
    for field, rule in rules.items():
        if field in row:
            try:
                if float(row[field]) > float(rule['max']):
                    issues.append(f"{field} exceeds {rule['max']}")
            except ValueError:
                continue
    return issues
