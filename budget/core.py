"""Core business logic for the budget CLI app."""


def add_transaction(transactions: list[dict], transaction: dict) -> list[dict]:
    """Add a transaction to the transaction list and return the updated list."""
    pass


def get_balance(transactions: list[dict]) -> int:
    """Return the net balance for the provided transactions."""
    pass


def filter_by_category(transactions: list[dict], category: str) -> list[dict]:
    """Return transactions matching the given category."""
    pass


def load_transactions_from_csv(file_path: str) -> list[dict]:
    """Load transactions from a CSV file and return them as a list of dicts."""
    pass


def monthly_summary(transactions: list[dict]) -> dict[str, dict[str, int]]:
    """Return a monthly income, expense, and net summary."""
    pass

