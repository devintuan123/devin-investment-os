from __future__ import annotations

import ast
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
STORE = ROOT_DIR / "utils" / "portfolio_store.py"
PORTFOLIO_MODULE = ROOT_DIR / "modules" / "portfolio" / "__init__.py"


def main() -> int:
    findings = []
    if not STORE.exists():
        findings.append("utils/portfolio_store.py missing")
    else:
        tree = ast.parse(STORE.read_text(encoding="utf-8"))
        functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        required = {"load_portfolio", "save_portfolio", "backup_portfolio", "clear_portfolio", "add_holding", "reduce_holding", "close_holding", "delete_holding", "record_transaction", "load_transactions", "calculate_realized_pl", "validate_portfolio_row", "normalize_symbol"}
        missing = sorted(required - functions)
        if missing:
            findings.append("Missing portfolio_store functions: " + ", ".join(missing))
    if not (ROOT_DIR / "data" / "transactions.csv").exists():
        findings.append("data/transactions.csv missing")
    if not PORTFOLIO_MODULE.exists():
        findings.append("modules/portfolio/__init__.py missing")
    else:
        source = PORTFOLIO_MODULE.read_text(encoding="utf-8")
        for term in ["confirm_clear_holdings", "clear_portfolio", "add_holding", "reduce_holding", "close_holding", "load_transactions"]:
            if term not in source:
                findings.append(f"Portfolio UI missing {term}")
        forbidden = ["place_order", "submit_order", "withdraw", "futures", "margin"]
        for term in forbidden:
            if term in source.lower() or (STORE.exists() and term in STORE.read_text(encoding="utf-8").lower()):
                findings.append(f"Forbidden broker execution language found: {term}")
    if findings:
        print("FAIL portfolio management gate")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PASS portfolio management gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
