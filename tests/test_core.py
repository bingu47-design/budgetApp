"""Tests for budget.core."""

from budget.core import (
    add_transaction,
    filter_by_category,
    get_balance,
    load_transactions_from_csv,
    monthly_summary,
)


def test_add_transaction_increases_length() -> None:
    """Adding a transaction should increase the list length by one."""
    transactions = []
    transaction = {
        "date": "2026-01-07",
        "type": "수입",
        "category": "급여",
        "description": "월급",
        "amount": 3500000,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1


def test_add_transaction_preserves_negative_amount() -> None:
    """Expense transactions should keep a negative amount."""
    transactions = []
    transaction = {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["amount"] == -12000


def test_add_transaction_preserves_positive_amount() -> None:
    """Income transactions should keep a positive amount."""
    transactions = []
    transaction = {
        "date": "2026-01-28",
        "type": "기타수입",
        "category": "기타수입",
        "description": "중고 판매",
        "amount": 25000,
        "memo": "중고마켓",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["amount"] == 25000


def test_add_transaction_allows_empty_description() -> None:
    """Transactions should allow an empty description."""
    transactions = []
    transaction = {
        "date": "2026-01-12",
        "type": "지출",
        "category": "식비",
        "description": "",
        "amount": -5800,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["description"] == ""


def test_get_balance_returns_zero_for_empty_list() -> None:
    """An empty transaction list should produce a zero balance."""
    transactions: list[dict] = []

    result = get_balance(transactions)

    assert result == 0.0


def test_get_balance_sums_real_step2_transactions() -> None:
    """Step 2 CSV-shaped transactions should sum to the expected balance."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-15",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 135541,
            "memo": "",
        },
        {
            "date": "2026-02-01",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 4358625,
            "memo": "",
        },
        {
            "date": "2026-03-11",
            "type": "지출",
            "category": "쇼핑",
            "description": "옷 구입",
            "amount": -39971,
            "memo": "카드결제",
        },
    ]

    result = get_balance(transactions)

    assert result == 3474399


def test_filter_by_category_matches_case_insensitively() -> None:
    """Category matching should ignore case for ASCII input."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "의료",
            "description": "한의원",
            "amount": -65990,
            "memo": "카드결제",
        },
    ]

    result = filter_by_category(transactions, "여행")

    assert len(result) == 1
    assert result[0]["category"] == "여행"


def test_filter_by_category_returns_empty_list_for_missing_category() -> None:
    """Unknown categories should return an empty list."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        }
    ]

    result = filter_by_category(transactions, "식비")

    assert result == []


def test_filter_by_category_returns_independent_list() -> None:
    """The filtered result should not mutate the original transaction list."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        }
    ]

    result = filter_by_category(transactions, "여행")
    result.append(
        {
            "date": "2026-01-99",
            "type": "지출",
            "category": "여행",
            "description": "추가",
            "amount": -1,
            "memo": "",
        }
    )

    assert len(transactions) == 1
    assert len(result) == 2


def test_load_transactions_from_csv_reads_step1_transactions() -> None:
    """Step 1 CSV should load the expected transaction dictionaries."""
    result = load_transactions_from_csv("data/step1_transactions.csv")

    assert len(result) == 10
    assert result[0] == {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }
    assert result[-1] == {
        "date": "2026-01-28",
        "type": "기타수입",
        "category": "기타수입",
        "description": "중고 판매",
        "amount": 25000,
        "memo": "중고마켓",
    }
    assert all(
        isinstance(transaction["amount"], int)
        for transaction in result
    )


def test_monthly_summary_aggregates_income_expense_and_net() -> None:
    """Monthly summary should group totals by YYYY-MM."""
    transactions = [
        {
            "date": "2026-01-05",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 3500000,
            "memo": "",
        },
        {
            "date": "2026-01-10",
            "type": "지출",
            "category": "식비",
            "description": "점심식사",
            "amount": -12000,
            "memo": "",
        },
        {
            "date": "2026-02-01",
            "type": "기타수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 25000,
            "memo": "중고마켓",
        },
    ]

    result = monthly_summary(transactions)

    assert result == {
        "2026-01": {"income": 3500000, "expense": -12000, "net": 3488000},
        "2026-02": {"income": 25000, "expense": 0, "net": 25000},
    }
