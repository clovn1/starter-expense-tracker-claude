from expense_tracker.commands import add, total
from tests.conftest import args, make_store


def _seed(store):
    add.handle(args(amount="10.00", category="food", date="2026-01-01", note=""), store)
    add.handle(args(amount="40.00", category="travel", date="2026-01-02", note=""), store)
    add.handle(args(amount="12.50", category="food", date="2026-01-03", note=""), store)


def test_total_all(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    code = total.handle(args(category=None), store)
    out = capsys.readouterr().out
    assert code == 0
    assert out == "$62.50\n"


def test_total_filtered_by_category(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    code = total.handle(args(category="food"), store)
    out = capsys.readouterr().out
    assert code == 0
    assert out == "$22.50\n"


def test_total_empty(tmp_path, capsys):
    store = make_store(tmp_path)
    code = total.handle(args(category=None), store)
    out = capsys.readouterr().out
    assert code == 0
    assert out == "$0.00\n"


def test_total_no_matching_category(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    code = total.handle(args(category="rent"), store)
    out = capsys.readouterr().out
    assert code == 0
    assert out == "$0.00\n"


def test_total_does_not_modify_store(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    before = store.load()
    total.handle(args(category=None), store)
    assert store.load() == before
