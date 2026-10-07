"""The ``total`` command: show the sum of recorded expenses."""

from __future__ import annotations

from ..money import format_amount

NAME = "total"
HELP = "Show the total of all expenses, optionally filtered by category"


def add_parser(subparsers) -> None:
    parser = subparsers.add_parser(NAME, help=HELP)
    parser.add_argument(
        "--category",
        default=None,
        help="Only total expenses in this category",
    )


def handle(args, store) -> int:
    expenses = store.load()
    if args.category is not None:
        expenses = [e for e in expenses if e.category == args.category]

    total_cents = sum(e.amount_cents for e in expenses)
    print(format_amount(total_cents))
    return 0
