def format_currency(value):
    return f"₹{value:,.2f}"

def percentage_change(old, new):
    try:
        return ((new - old) / old) * 100
    except ZeroDivisionError:
        return float('inf')
