import numbers
import random
import regex

ROLL_REGEX = r'(?P<num>\d+)d(?P<die>\d+)(?P<keep>kl?\d*)?(?P<mod>[\+\-]\d+)?'


class Roll(numbers.Number):
    def __init__(self, value):
        self.value = value
        self.used = True

    def __str__(self):
        if self.used:
            return str(self.value)
        else:
            return '~~%d~~' % self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        return '<Roll: %d>' % self.value

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Roll((self.value if self.used else 0) + other)
        elif isinstance(other, Roll):
            return (self.value if self.used else 0) + (other.value if other.used else 0)
        elif isinstance(other, str):
            return str(self) + other
        else:
            raise TypeError

    def __radd__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, Roll):
            return self + other
        elif isinstance(other, str):
            return other + str(self)
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Roll(self.value - other)
        elif isinstance(other, Roll):
            return Roll(self.value - other.value)
        else:
            raise TypeError

    def __rsub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Roll(other - self.value)
        elif isinstance(other, Roll):
            return Roll(other.value - self.value)

    def __eq__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.value == other
        elif isinstance(other, Roll):
            return self.value == other.value
        else:
            raise TypeError

    def __gt__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.value > other
        elif isinstance(other, Roll):
            return self.value > other.value
        else:
            raise TypeError


def roll(string: str) -> str:
    match = regex.match(ROLL_REGEX, string)
    groups = match.capturesdict()
    num = int(groups['num'][0])
    die = int(groups['die'][0])
    results = []

    for x in range(num):
        results.append(Roll(random.randint(1, die)))

    if len(groups['keep']) == 1:
        keep = groups['keep'][0]
        highest = not keep.startswith('kl')
        if keep == 'kl' or keep == 'k':
            val = 1
        else:
            val = int(keep[(1 if highest else 2):])
        for result in sorted(results, reverse=highest)[val:]:
            result.used = False

    total = sum(results)

    out = '(' + ' + '.join(map(str, results)) + ')'
    if len(groups['mod']) == 1:
        out += ' ' + groups['mod'][0]
        total += int(groups['mod'][0])
    out += ' = ' + str(total)
    return out
