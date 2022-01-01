from __future__ import annotations
import argparse
from dataclasses import dataclass
import csv
import datetime
from typing import List, Mapping, Any


@dataclass(frozen=True)
class RuleEntry:
    """Text to be in transaction description for the transaction to be categorized as trg_category"""
    src_substring: str
    """Category to categorize the transaction having substring src_substring"""
    trg_category: str

    @staticmethod
    def from_csv_row(row: Mapping[str, Any]) -> RuleEntry:
        return RuleEntry(src_substring=row["SRC_SUBSTRING"], trg_category=row["TRG_CATEGORY"])


@dataclass(frozen=True)
class TransactionEntry:
    date: datetime.date
    description: str
    ccy: str
    amount_in_ccy: float
    acc_ccy: str
    amount_in_acc_ccy: float

    @staticmethod
    def from_csv_row(row: Mapping[str, Any]) -> TransactionEntry:
        return TransactionEntry(
            date=parse_date(row["Дата транзакции"]),
            description=row["Описание"],
            ccy=row["Валюта операции"],
            amount_in_ccy=parse_num(row["Сумма в валюте операции"]),
            acc_ccy=row["Валюта счета"],
            amount_in_acc_ccy=parse_num(row["Сумма в валюте счета"]),
        )


def parse_num(str_num: str) -> float:
    return float(str_num.replace(' ', ''))


def parse_date(str_date: str) -> datetime.date:
    """parses string like 31.12.2021 00:00"""
    day = int(str_date[0:2])
    month = int(str_date[3:5])
    year = int(str_date[6:10])
    return datetime.date(year, month, day)


def main():
    parser = argparse.ArgumentParser(
        description="Tries to categorize Raiffeisenbank Russia CSV export transactions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--rules-file",
                        help="CSV file whose first column is transaction substring and second column is target category",
                        metavar="RULES_FILE")
    parser.add_argument("transactions", metavar="TRANS_FILES")

    args = parser.parse_args()

    rules = get_rules(args.rules_file)
    transactions = get_transactions(args.transactions)
    print(f"Found {len(rules)} rules and {len(transactions)} transactions")
    categories_to_transactions = categorize(transactions, rules)
    print(f"Processed {sum((len(trans) for trans in categories_to_transactions.values()))} transactions")
    print("=======================================================")
    print_report(categories_to_transactions)


def categorize(transactions: List[TransactionEntry], rules: List[RuleEntry]) -> Mapping[str, List[TransactionEntry]]:
    category_to_transactions = {}
    for t in transactions:
        category = categorize_tran(t, rules)
        if category not in category_to_transactions:
            category_to_transactions[category] = []
        category_to_transactions[category].append(t)
    return category_to_transactions


def categorize_tran(transaction: TransactionEntry, rules: List[RuleEntry]) -> str:
    desc = transaction.description
    for r in rules:
        if r.src_substring in desc:
            return r.trg_category
    return UNCATEGORIZED


UNCATEGORIZED = "UNCATEGORIZED"


def print_report(categories_to_transactions: Mapping[str, List[TransactionEntry]]) -> None:
    for (category, transactions) in categories_to_transactions.items():
        acc_ccy = transactions[0].acc_ccy
        total_in_acc = sum((t.amount_in_acc_ccy for t in transactions))
        print(f"For category {category} (total {total_in_acc:.2f} {acc_ccy}):")
        print("-------------------------------------------------------")
        for t in transactions:
            print(f"{t.date};{t.description};{t.amount_in_acc_ccy:.2f};{t.acc_ccy}")
        print("=======================================================")
    pass


def get_rules(rules_file) -> List[RuleEntry]:
    rules: List[RuleEntry] = []
    with open(rules_file, 'r', newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            rules.append(RuleEntry.from_csv_row(row))
    return rules


def get_transactions(transactions_file) -> List[TransactionEntry]:
    transactions: List[TransactionEntry] = []
    with open(transactions_file, 'r', newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            transactions.append(TransactionEntry.from_csv_row(row))
    return transactions


if __name__ == "__main__":
    main()
