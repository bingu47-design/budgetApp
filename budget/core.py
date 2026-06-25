"""Core business logic for the budget CLI app."""

from csv import DictReader


def add_transaction(transactions: list[dict], transaction: dict) -> list[dict]:
    """Add a transaction to the transaction list and return the updated list."""
    updated_transactions = transactions.copy()
    updated_transactions.append(transaction)
    return updated_transactions


def get_balance(transactions: list[dict]) -> float:
    """Return the net balance for the provided transactions."""
    balance = 0.0
    for transaction in transactions:
        balance += transaction["amount"]
    return balance


def filter_by_category(transactions: list[dict], category: str) -> list[dict]:
    """Return transactions matching the given category."""
    normalized_category = category.casefold()
    filtered_transactions = []
    for transaction in transactions:
        if transaction["category"].casefold() == normalized_category:
            filtered_transactions.append(transaction)
    return filtered_transactions


def load_transactions_from_csv(file_path: str) -> list[dict]:
    """Load transactions from a CSV file and return them as a list of dicts."""
    transactions = []
    with open(file_path, encoding="utf-8-sig", newline="") as csv_file:
        reader = DictReader(csv_file)
        for row in reader:
            transactions.append(
                {
                    "date": row["date"],
                    "type": row["type"],
                    "category": row["category"],
                    "description": row["description"],
                    "amount": int(row["amount"]),
                    "memo": row["memo"],
                }
            )
    return transactions


def monthly_summary(transactions: list[dict]) -> dict[str, dict[str, int]]:
    """Return a monthly income, expense, and net summary."""
    summary: dict[str, dict[str, int]] = {}
    for transaction in transactions:
        month = transaction["date"][:7]
        if month not in summary:
            summary[month] = {"income": 0, "expense": 0, "net": 0}
        amount = transaction["amount"]
        if amount > 0:
            summary[month]["income"] += amount
        else:
            summary[month]["expense"] += amount
        summary[month]["net"] += amount
    return summary
