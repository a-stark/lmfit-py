import numpy as np
from numpy.testing import assert_allclose

import lmfit
from lmfit_testutils import assert_paramval

def residual(params, x, data):
    return data - 1.0/(params['a']*x)+ params['b']

def residual2(params, x, data):
    return data - params['c']/(params['a']*x)+params['b']

def test_confidence1():
    x = np.linspace(0.3,10,100)
    np.random.seed(0)

    y = 1/(0.1*x)+2+0.1*np.random.randn(x.size)

    pars = lmfit.Parameters()
    pars.add_many(('a', 0.1), ('b', 1))

    minimizer = lmfit.Minimizer(residual, pars, fcn_args=(x, y) )
    out = minimizer.leastsq()
    # lmfit.report_fit(out)

    assert(out.nfev >   5)
    assert(out.nfev < 500)
    assert(out.chisqr < 3.0)
    assert(out.nvarys == 2)

    assert_paramval(out.params['a'],  0.1, tol=0.1)
    assert_paramval(out.params['b'], -2.0, tol=0.1)

    ci = lmfit.conf_interval(minimizer, out)
    assert_allclose(ci['b'][0][0],  0.997,  rtol=0.01)
    assert_allclose(ci['b'][0][1], -2.022,  rtol=0.01)
    assert_allclose(ci['b'][2][0],  0.683,  rtol=0.01)
    assert_allclose(ci['b'][2][1], -1.997,  rtol=0.01)
    assert_allclose(ci['b'][5][0],  0.95,   rtol=0.01)
    assert_allclose(ci['b'][5][1], -1.96,   rtol=0.01)

   # lmfit.printfuncs.report_ci(ci)


def test_confidence2():
    x = np.linspace(0.3,10,100)
    np.random.seed(0)

    y = 1/(0.1*x)+2+0.1*np.random.randn(x.size)

    pars = lmfit.Parameters()
    pars.add_many(('a', 0.1), ('b', 1), ('c', 1.0))
    pars['a'].max = 0.25
    pars['a'].min = 0.00
    pars['a'].value = 0.2
    pars['c'].vary = False

    minimizer = lmfit.Minimizer(residual2, pars, fcn_args=(x, y) )
    out = minimizer.minimize(method='nelder')
    out = minimizer.minimize(method='leastsq', params=out.params)
    # lmfit.report_fit(out)

    assert(out.nfev >   5)
    assert(out.nfev < 500)
    assert(out.chisqr < 3.0)
    assert(out.nvarys == 2)

    assert_paramval(out.params['a'],  0.1, tol=0.1)
    assert_paramval(out.params['b'], -2.0, tol=0.1)

    ci = lmfit.conf_interval(minimizer, out)
    assert_allclose(ci['b'][0][0],  0.997,  rtol=0.01)
    assert_allclose(ci['b'][0][1], -2.022,  rtol=0.01)
    assert_allclose(ci['b'][2][0],  0.683,  rtol=0.01)
    assert_allclose(ci['b'][2][1], -1.997,  rtol=0.01)
    assert_allclose(ci['b'][5][0],  0.95,   rtol=0.01)
    assert_allclose(ci['b'][5][1], -1.96,   rtol=0.01)

    lmfit.printfuncs.report_ci(ci)

if __name__ == '__main__':
    test_confidence1()
    test_confidence2()
