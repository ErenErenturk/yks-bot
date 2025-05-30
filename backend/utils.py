# utils.py

def format_percentage(count: int, total: int) -> str:
    if total == 0:
        return "0.0"
    return f"{100 * count / total:.1f}"
