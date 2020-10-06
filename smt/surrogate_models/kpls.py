"""
Author: Dr. Mohamed A. Bouhlel <mbouhlel@umich.edu>

This package is distributed under New BSD license.
"""
import warnings
import numpy as np

from packaging import version
from sklearn import __version__ as sklversion

if version.parse(sklversion) < version.parse("0.22"):
    from sklearn.cross_decomposition.pls_ import PLSRegression as pls
else:
    from sklearn.cross_decomposition import PLSRegression as pls

from smt.surrogate_models.krg_based import KrgBased
from smt.utils.kriging_utils import componentwise_distance_PLS


class KPLS(KrgBased):
    def _initialize(self):
        super(KPLS, self)._initialize()
        declare = self.options.declare
        declare("n_comp", 1, types=int, desc="Number of principal components")
        self.name = "KPLS"

    def _compute_pls(self, X, y):
        _pls = pls(self.options["n_comp"])
        self.coeff_pls = _pls.fit(X.copy(), y.copy()).x_rotations_

        return X, y

    def _componentwise_distance(self, dx, opt=0):
        d = componentwise_distance_PLS(
            dx, self.options["corr"], self.options["n_comp"], self.coeff_pls
        )
        return d
