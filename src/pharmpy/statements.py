import sympy


class Assignment:
    """Representation of variable assignment
       similar to sympy.codegen.Assignment
    """
    def __init__(self, symbol, expression):
        """ symbol can be either string or sympy symbol
            symbol can be a string and a real symbol will be created
        """
        try:
            symbol.is_Symbol
            self.symbol = symbol
        except AttributeError:
            self.symbol = sympy.Symbol(symbol, real=True)
        self.expression = expression

    def subs(self, old, new):
        """Substitute old into new of rhs. Inplace
        """
        self.expression = self.expression.subs(old, new)

    @property
    def free_symbols(self):
        symbols = {self.symbol}
        symbols |= self.expression.free_symbols
        return symbols

    def __str__(self):
        return f'{self.symbol} := {self.expression}'


class Compartment:
    def __init__(self, name, input, output, amount, volume):
        self.name = name
        self.input = input
        self.output = output
        self.amount = amount
        self.volume = volume

    @property
    def free_symbols(self):
        return self.input.free_symbols | self.output.free_symbols | self.amount.free_symbols | \
               self.volume.free_symbols

    def __repr__(self):
        return f'{self.amount} := compartment({self.name}, input={self.input}, ' \
               f'output={self.output}, amount={self.amount}, volume={self.volume})'


class IVAbsorption:
    def __init__(self, data_label):
        self.data_label = data_label

    @property
    def free_symbols(self):
        return set()

    def __repr__(self):
        return f'IVAbsorption({self.data_label})'


class Elimination:
    def __init__(self, rate):
        self.rate = rate

    @property
    def free_symbols(self):
        return self.rate.free_symbols

    def __repr__(self):
        return f'Elimination({self.rate})'


class ModelStatements(list):
    """A list of sympy statements describing the model
    """
    @property
    def free_symbols(self):
        """Get a set of all free symbols"""
        symbols = set()
        for assignment in self:
            symbols |= assignment.free_symbols
        return symbols

    def subs(self, old, new):
        """Substitute old expression for new in all rhs of assignments"""
        for assignment in self:
            assignment.subs(old, new)

    def __str__(self):
        s = [str(assignment) for assignment in self]
        return '\n'.join(s)
