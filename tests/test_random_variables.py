import pytest
import sympy
import sympy.stats as stats

from pharmpy.random_variables import JointNormalSeparate, RandomVariables


def test_joint_normal_separate():
    rvs = JointNormalSeparate(['ETA(1)', 'ETA(2)'], [0, 0], [[1, 0], [0, 1]])
    assert rvs[0].name == 'ETA(1)'
    assert rvs[1].name == 'ETA(2)'
    assert rvs[0].pspace.distribution.mu == sympy.Matrix([[0], [0]])
    assert rvs[0].pspace.distribution.sigma == sympy.Matrix([[1, 0], [0, 1]])
    assert stats.random_symbols(rvs[0]) == [rvs[0]]
    assert stats.random_symbols(rvs[1]) == [rvs[1]]

    rvs2 = JointNormalSeparate(['ETA(3)', 'ETA(4)'], [1, 1], [[6, 3], [4, 5]])
    # Check that previously created rvs are still intact
    assert rvs[0].name == 'ETA(1)'
    assert rvs[1].name == 'ETA(2)'
    assert rvs[0].pspace.distribution.mu == sympy.Matrix([[0], [0]])
    assert rvs[0].pspace.distribution.sigma == sympy.Matrix([[1, 0], [0, 1]])
    assert stats.random_symbols(rvs[0]) == [rvs[0]]
    assert stats.random_symbols(rvs[1]) == [rvs[1]]
    assert len(rvs2) == 2


def test_rv():
    omega1 = sympy.Symbol('OMEGA(1,1)')
    x = stats.Normal('ETA(1)', 0, sympy.sqrt(omega1))
    rvs = RandomVariables([x])
    assert len(rvs) == 1
    retrieved = rvs['ETA(1)']
    assert retrieved.name == 'ETA(1)'
    assert retrieved.pspace.distribution.mean == 0


def test_distributions():
    rvs = JointNormalSeparate(['ETA(1)', 'ETA(2)'], [0, 0], [[3, 0.25], [0.25, 1]])
    rvs = RandomVariables(rvs)
    rvs.add(stats.Normal('ETA(3)', 0.5, 2))
    gen = rvs.distributions()
    symbols, dist = next(gen)
    assert symbols[0].name == 'ETA(1)'
    assert symbols[1].name == 'ETA(2)'
    assert len(symbols) == 2
    assert dist == rvs[0].pspace.distribution
    symbols, dist = next(gen)
    assert symbols[0].name == 'ETA(3)'
    assert len(symbols) == 1
    assert dist == rvs[2].pspace.distribution
    with pytest.raises(StopIteration):
        symbols, dist = next(gen)


def test_merge_normal_distributions():
    rvs = JointNormalSeparate(['ETA(1)', 'ETA(2)'], [0, 0], [[3, 0.25], [0.25, 1]])
    rvs = RandomVariables(rvs)
    rvs.add(stats.Normal('ETA(3)', 0.5, 2))
    rvs.merge_normal_distributions()
    assert len(rvs) == 3
    assert rvs['ETA(1)'].name == 'ETA(1)'
    assert rvs[1].name == 'ETA(2)'
    assert rvs[2].name == 'ETA(3)'
    assert rvs[0].pspace is rvs[1].pspace
    assert rvs[0].pspace is rvs[2].pspace
    dist = rvs[0].pspace.distribution
    assert dist.mu == sympy.Matrix([0, 0, 0.5])
    assert dist.sigma == sympy.Matrix([[3, 0.25, 0], [0.25, 1, 0], [0, 0, 4]])
    rvs.merge_normal_distributions(fill=1)
    dist = rvs[0].pspace.distribution
    assert dist.sigma == sympy.Matrix([[3, 0.25, 1], [0.25, 1, 1], [1, 1, 4]])


def test_validate_parameters():
    a, b, c, d = sympy.symbols('a b c d')
    rvs = JointNormalSeparate(['ETA(1)', 'ETA(2)'], [0, 0], [[a, b], [b, c]])
    rvs = RandomVariables(rvs)
    rvs.add(stats.Normal('ETA(3)', 0.5, d))
    params = {'a': 2, 'b': 0.1, 'c': 1, 'd': 23}
    assert rvs.validate_parameters(params)
    params2 = {'a': 2, 'b': 2, 'c': 1, 'd': 23}
    assert not rvs.validate_parameters(params2)
