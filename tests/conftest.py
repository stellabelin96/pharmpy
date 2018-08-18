
import csv
import random
import re
import string
from collections import namedtuple
from pathlib import Path

import pytest

tuple_matcher = re.compile(r'^\((.*)\)$')


@pytest.fixture(scope='session')
def testdata():
    return Path(__file__).resolve().parent / 'testdata'


# @pytest.fixture(scope='session')
# def SOURCE():
#     return Path(__file__).resolve().parent.parent / 'src'


@pytest.fixture(scope='session')
def csv_read():
    def func(root, file, names=None):
        TestData = tuple
        if names:
            TestData = namedtuple('TestData', names)

        def descape(item):
            return item.replace('\\n', '\n')

        def tupleize(item):
            m = tuple_matcher.match(item)
            if not m:
                return descape(item)
            if not m.group(1):
                return ()
            return tuple(descape(x.strip(' "')) for x in m.group(1).split(','))

        with open(Path(root, file), 'r') as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0)
            reader = csv.reader(f, dialect)
            return tuple(TestData(*tuple(map(tupleize, row))) for row in reader)

    return func


@pytest.fixture(scope='session')
def str_repr():
    def func(string):
        if not string:
            return '-- EMPTY --'
        return '"' + repr(string)[1:-1] + '"'
    return func


class Random:
    _history = []
    values = []

    def __new__(cls, *a, **kw):
        if cls.values:
            cls._history += [cls.values]
            cls.values = []
        obj = super(Random, cls).__new__(cls)
        obj.__init__(*a, **kw)
        return obj

    def __init__(self, length=None):
        self.length = length

    def pos_int(self, size=1E6):
        return self._gen(random.randint, 0, size)

    def int(self, size=1E6):
        return self._gen(random.randint, -size, size)

    def float(self, size=1E9):
        return self._gen(random.normalvariate, 0, size)

    def str(self, charlen=30, chars=string.printable):
        def f(ch, l):
            return ''.join(random.choice(ch) for _ in range(l))
        return self._gen(f, chars, charlen)

    def pad(self, maxlen=5, nl=False):
        chars = ' '
        if nl:
            chars += '\n'

        def f(l):
            return random.choice(chars)*random.choice([0]*l + list(range(1, l)))
        return self._gen(f, maxlen)

    def _gen(self, f, *args, **kwargs):
        while len(self.values) != self.length:
            self.values += [f(*args, **kwargs)]
            yield self.values[-1]

    def __str__(self):
        rval = ', '.join(repr(x) for x in self.values)
        return '%s(%d): %s' % (self.__class__.__name__, self.length, rval)

    @classmethod
    def history(cls):
        out = []
        for i, hist in enumerate(cls._history):
            out += ['[%d] %s' % (i, ', '.join(repr(x) for x in hist))]
        return '\n'.join(out)


@pytest.fixture(scope='class')
def random_data(request):
    request.cls.data = Random
    yield