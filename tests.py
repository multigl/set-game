import pytest
import sets


@pytest.mark.parametrize('raw,expected', (
        ('#', 1),
        ('$', 1),
        ('AA', 2),
        ('@', 1),
        ('@@@', 3),
        ('A', 1),
        ('$$$', 3),
        ('@@@', 3),
        ('HHH', 3),
        ('#', 1),
        ('@@', 2),
        ('a', 1),
        ('sss', 3),
        ('a', 1),
        ('@', 1),
))
def test_infer_count(raw, expected):
    assert sets.infer_count(raw) == expected


@pytest.mark.parametrize('raw,expected', (
        ('#', sets.Shades.outlined),
        ('$', sets.Shades.outlined),
        ('AA', sets.Shades.solid),
        ('@', sets.Shades.outlined),
        ('@@@', sets.Shades.outlined),
        ('A', sets.Shades.solid),
        ('$$$', sets.Shades.outlined),
        ('@@@', sets.Shades.outlined),
        ('HHH', sets.Shades.solid),
        ('#', sets.Shades.outlined),
        ('@@', sets.Shades.outlined),
        ('a', sets.Shades.striped),
        ('sss', sets.Shades.striped),
        ('a', sets.Shades.striped),
        ('@', sets.Shades.outlined),
))
def test_shade_from_raw(raw, expected):
    assert sets.Shades.from_raw(raw) == expected


@pytest.mark.parametrize('raw,expected', (
        ('#', sets.Symbols.H),
        ('$', sets.Symbols.S),
        ('AA', sets.Symbols.A),
        ('@', sets.Symbols.A),
        ('@@@', sets.Symbols.A),
        ('A', sets.Symbols.A),
        ('$$$', sets.Symbols.S),
        ('@@@', sets.Symbols.A),
        ('HHH', sets.Symbols.H),
        ('#', sets.Symbols.H),
        ('@@', sets.Symbols.A),
        ('a', sets.Symbols.A),
        ('sss', sets.Symbols.S),
        ('a', sets.Symbols.A),
        ('@', sets.Symbols.A),
))
def test_symbol_from_raw(raw, expected):
    assert sets.Symbols.from_raw(raw) == expected


@pytest.mark.parametrize('raw,expected', (
        ('blue #', (sets.Colors.blue, sets.Symbols.H, sets.Shades.outlined, 1)),
        ('green $', (sets.Colors.green, sets.Symbols.S, sets.Shades.outlined, 1)),
        ('blue AA', (sets.Colors.blue, sets.Symbols.A, sets.Shades.solid, 2)),
        ('yellow @', (sets.Colors.yellow, sets.Symbols.A, sets.Shades.outlined, 1)),
        ('blue @@@', (sets.Colors.blue, sets.Symbols.A, sets.Shades.outlined, 3)),
        ('green A', (sets.Colors.green, sets.Symbols.A, sets.Shades.solid, 1)),
        ('yellow $$$', (sets.Colors.yellow, sets.Symbols.S, sets.Shades.outlined, 3)),
        ('yellow @@@', (sets.Colors.yellow, sets.Symbols.A, sets.Shades.outlined, 3)),
        ('yellow HHH', (sets.Colors.yellow, sets.Symbols.H, sets.Shades.solid, 3)),
        ('yellow #', (sets.Colors.yellow, sets.Symbols.H, sets.Shades.outlined, 1)),
        ('yellow @@', (sets.Colors.yellow, sets.Symbols.A, sets.Shades.outlined, 2)),
        ('blue a', (sets.Colors.blue, sets.Symbols.A, sets.Shades.striped, 1)),
        ('blue sss', (sets.Colors.blue, sets.Symbols.S, sets.Shades.striped, 3)),
        ('green a', (sets.Colors.green, sets.Symbols.A, sets.Shades.striped, 1)),
        ('green @', (sets.Colors.green, sets.Symbols.A, sets.Shades.outlined, 1)),
))
def test_make_card(raw, expected):
    assert sets.Card.from_raw(raw) == expected


@pytest.mark.parametrize('cards,is_set', (
        ([
            sets.Card.from_raw('blue H'),
            sets.Card.from_raw('green S'),
            sets.Card.from_raw('yellow A')
         ], True),
        ([
            sets.Card.from_raw('green $'),
            sets.Card.from_raw('green $$'),
            sets.Card.from_raw('green $$$')
         ], True),
        ([
            sets.Card.from_raw('yellow $​'),
            sets.Card.from_raw('blue H'),
            sets.Card.from_raw('green aa')
         ], False),
        ([
            sets.Card.from_raw('green HHH'),
            sets.Card.from_raw('blue hhh'),
            sets.Card.from_raw('blue HHH')
         ], False),

))
def test_valid_set(cards, is_set):
    assert sets.valid_set(cards) == is_set


def test_find_sets():
    deck = [
        sets.Card.from_raw('blue #'),
        sets.Card.from_raw('green $'),
        sets.Card.from_raw('blue AA'),
        sets.Card.from_raw('yellow @'),
        sets.Card.from_raw('blue @@@'),
        sets.Card.from_raw('green A'),
        sets.Card.from_raw('yellow $$$'),
        sets.Card.from_raw('yellow @@@'),
        sets.Card.from_raw('yellow HHH'),
        sets.Card.from_raw('yellow #'),
        sets.Card.from_raw('yellow @@'),
        sets.Card.from_raw('blue a'),
        sets.Card.from_raw('blue sss'),
        sets.Card.from_raw('green a'),
        sets.Card.from_raw('green @'),
    ]

    expected_sets = [
        {sets.Card.from_raw('blue #'), sets.Card.from_raw('green $'), sets.Card.from_raw('yellow @')},
        {sets.Card.from_raw('blue a'), sets.Card.from_raw('blue AA'), sets.Card.from_raw('blue @@@')},
        {sets.Card.from_raw('green a'), sets.Card.from_raw('green A'), sets.Card.from_raw('green @')},
        {sets.Card.from_raw('yellow #'), sets.Card.from_raw('yellow @@'), sets.Card.from_raw('yellow $$$')}
    ]

    found_sets = sets.find_sets(deck)
    assert len(found_sets) == 9
    for expected_set in expected_sets:
        assert expected_set in found_sets
