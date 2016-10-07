import typing
import itertools, collections
import enum


class Card(collections.namedtuple('card', ('color', 'symbol', 'shade', 'number'))):
    def __repr__(self):
        raw, = self.symbol.value & self.shade.value

        return "sets.Card.from_raw('{} {}')".format(self.color.name, raw * self.number)

    @classmethod
    def from_raw(cls, raw):
        color, attrs = raw.split(' ')
        return cls(Colors[color], Symbols.from_raw(attrs), Shades.from_raw(attrs), infer_count(attrs))


class Colors(enum.Enum):
    blue = "blue"
    green = "green"
    yellow = "yellow"


class Symbols(enum.Enum):
    A = frozenset(['a', 'A', '@'])
    S = frozenset(['s', 'S', '$'])
    H = frozenset(['h', 'H', '#'])

    @classmethod
    def from_raw(cls, raw: str):
        symbol = next(k for k in cls if raw[0] in k.value)
        assert symbol, "invalid symbol: {}".format(raw)
        return symbol


class Shades(enum.Enum):
    solid = frozenset(['A', 'S', 'H'])
    outlined = frozenset(['$', '#', '@'])
    striped = frozenset(['h', 's', 'a'])

    @classmethod
    def from_raw(cls, raw: str):
        shade = next(k for k in cls if raw[0] in k.value)
        assert shade, "invalid shade: {}".format(raw)
        return shade


def infer_count(raw) -> int:
    return len(raw)


def valid_set(cards: typing.Set[Card]) -> bool:
    if not len(cards) is 3:
        return False

    valid_counts = frozenset([1, 3])  # all the same, or all different

    colors = len({c.color for c in cards}) in valid_counts
    symbols = len({c.symbol for c in cards}) in valid_counts
    shades = len({c.shade for c in cards}) in valid_counts
    numbers = len({c.number for c in cards}) in valid_counts

    return colors and symbols and shades and numbers


def find_sets(cards: typing.List[Card]) -> typing.List[typing.Set[Card]]:
    sets = []

    for combo in itertools.combinations(cards, 3):
        combo = set(combo)
        if not valid_set(combo):
            continue
        sets.append(combo)

    return sets
