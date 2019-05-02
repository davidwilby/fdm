# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import numpy as np
from numpy.testing import assert_allclose as close

from fdm import central_fdm, directional, gradient, jacobian, hvp
from fdm.multivariate import _get_at_index
# noinspection PyUnresolvedReferences
from . import eq, neq, lt, le, ge, gt, raises, ok


def test_get_index():
    yield raises, RuntimeError, lambda: _get_at_index(np.array(1), 1)


def test_gradient_vector_argument():
    m = central_fdm(10, 1)

    for a, x in zip([np.random.randn(),
                     np.random.randn(3),
                     np.random.randn(3, 3)],
                    [np.random.randn(),
                     np.random.randn(3),
                     np.random.randn(3, 3)]):
        def f(y):
            return np.sum(a * y * y)

        yield close, 2 * a * x, gradient(f, m)(x)


def test_directional():
    m = central_fdm(10, 1)
    a = np.random.randn(3)

    def f(x):
        return np.sum(a * x)

    x = np.random.randn(3)
    v = np.random.randn(3)
    yield close, np.sum(gradient(f, m)(x) * v), directional(f, v, m)(x)


def test_jacobian():
    m = central_fdm(10, 1)
    a = np.random.randn(3, 3)

    def f(x):
        return np.matmul(a, x)

    x = np.random.randn(3)
    yield close, jacobian(f, m)(x), a


def test_hvp():
    m_jac = central_fdm(10, 1, adapt=1)
    m_dir = central_fdm(10, 1, adapt=0)
    a = np.random.randn(3, 3)

    def f(x):
        return 0.5 * np.matmul(x, np.matmul(a, x))

    x = np.random.randn(3)
    v = np.random.randn(3)
    yield close, \
          hvp(f, v, jac_method=m_jac, dir_method=m_dir)(x), \
          np.matmul(0.5 * (a + a.T), v)[None, :]
