# AGENTS.md

## Project Overview
This repository is a Python CLI budget app project.
The app is CSV-based and is meant to manage transaction data, balances, category filtering, and monthly summaries from CSV files.

## Coding Rules
- Type hints are required for all functions and public data structures.
- A single function must be 50 lines or fewer.

## TDD Rules
- Implementations must always be driven by tests first.
- Write failing tests before writing production code.
- Do not consider a feature complete until the tests that describe it pass.

## Quality Rules
- Keep cyclomatic complexity at 10 or lower.

## Quality Review Rule
- Before any commit, the `qa_engineer` sub-agent must review the change for quality.

## Test Commands
- `pytest`
- `radon cc`

## Commit Rules
- When one feature is developed, commit it and push it.

