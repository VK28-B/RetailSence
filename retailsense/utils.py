# All of these go inside utils.py
import  json

def calculate_revenue(price, quantity, discount_pct=0):
    """
    Returns the final revenue after applying discount.
    Formula: price * quantity * (1 - discount_pct / 100)
    Default discount is 0%.
    """
    revenue = price * quantity * (1 - discount_pct / 100)
    return revenue


def classify_customer(age: float) -> str:
    """
    Returns customer segment as a string:
    - age < 25     → "Youth"
    - 25 <= age < 45 → "Adult"
    - age >= 45    → "Senior"
    - age is None  → "Unknown"
    Use type hints in your function signature.
    """
    segment = ""
    if age==None:
        segment = "Unknown"
    elif age>=25 and age <45:
        segment = "Adult"
    elif age>=45:
        segment = "Senior"
    elif age < 25:
        segment = "Youth"
    else:
        pass
    return segment


def is_valid_email(email: str) -> bool:
    """
    Returns True if email contains '@' and '.', else False.
    """
    email_valid = False
    if "@" in email and "." in email:
        email_valid = True
    return email_valid


def load_config(filepath: str) -> dict:
    """
    Reads a JSON file and returns it as a Python dictionary.
    Use a context manager (with block).
    """
    json_result = []
    with open(filepath, "r") as f:
        return json.load(f)


def write_summary_report(stats: dict, output_path: str) -> None:
    """
    Writes a plain-text summary report to the given file path.
    Each key-value pair in stats should be on its own line.
    Format: "Key: Value"
    Use a context manager (with block).
    """
    with open(output_path, "w") as f:
        for k,v in stats.items():
            f.write(f"{k}:{v}\n")

if __name__ == "__main__":
    print("Project name:-",load_config("config.json")['project_name'])
    print("Tax Rate:-",load_config("config.json")['tax_rate'])
    print("Final Revenue:-",calculate_revenue(1200, 3, 10))
    print("Age Segment:-",classify_customer(None))
