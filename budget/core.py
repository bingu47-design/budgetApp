"""Core business logic for the budget CLI app."""


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
    pass


def monthly_summary(transactions: list[dict]) -> dict[str, dict[str, int]]:
    """Return a monthly income, expense, and net summary."""
    pass
