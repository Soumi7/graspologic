# Copyright 2020 NeuroData (http://neurodata.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import abstractmethod
from sklearn.utils import check_array
from sklearn.base import BaseEstimator


class BaseAlign(BaseEstimator):
    """
    Base class for align tasks such as sign flipping, procrustes and seedless
    procrustes.

    Parameters
    ----------

    Attributes
    ----------
        Q_X : array, size (d, d)
              final orthogonal matrix, used to modify X

        Q_Y : array, size (d, d)
              final orthogonal matrix, used to modify Y

    """

    def __init__(self):
        pass

    @abstractmethod
    def fit(self, X, Y):
        """
        Uses the two datasets to learn matrices Q_X and Q_Y.

        Parameters
        ----------
        X: np.ndarray, shape (n, d)
            First dataset of vectors. These vectors need to have same number of
            dimensions as ones in Y, but the number of vectors can differ.

        Y: np.ndarray, shape (m, d)
            Second dataset of vectors. These vectors need to have same number
            of dimensions as ones in X, but the number of vectors can differ.

        Returns
        -------
        self: returns an instance of self
        """
        pass

    def transform(self, X, Y=None):
        """
        Uses the learned matrices Q_X, Q_Y to match the two datssets and
        returns them. These may or may not be the same datasets that it was fit
        to. Also supports only modifying the one dataset (the first one, X)
        dataset, by setting Y=None.

        Parameters
        ----------
        X: np.ndarray, shape (n, d)
            First dataset of vectors. These vectors need to have same number of
            dimensions as ones in Y, but the number of vectors can differ.

        Y: np.ndarray, shape (m, d) or None (default)
            Second dataset of vectors. These vectors need to have same number
            of dimensions as ones in X, but the number of vectors can differ.
            If None - only performs modifications to X.

        Returns
        -------
        X_prime: np.ndarray, shape (n, d)
            First dataset of vectors, matched to second. Equal to X @ self.Q_X.

        Y_prime: np.ndarray, shape (m, d)
            Second dataset of vectors, matched to first. Equal to X @ self.Q_Y,
            unless Y was set to None. In that case - it is not returned. #None?
        """
        X = check_array(X, copy=True)
        if Y is None:
            X_prime = X @ self.Q_X
            return (X_prime,)  # None # tried returning None, but felt clunky
        else:
            Y = check_array(Y, copy=True)
            X_prime, Y_prime = X @ self.Q_X, Y @ self.Q_Y
            return X_prime, Y_prime

    def fit_transform(self, X, Y):
        """
        Learns the matrices Q_X and Q_Y, uses them to match the two datasets
        provided, and returns the two matched datasets.

        Parameters
        ----------
        X: np.ndarray, shape (n, d)
            First dataset of vectors. These vectors need to have same number of
            dimensions as ones in Y, but the number of vectors can differ.

        Y: np.ndarray, shape (m, d)
            Second dataset of vectors. These vectors need to have same number
            of dimensions as ones in X, but the number of vectors can differ.

        Returns
        -------
        X_prime: np.ndarray, shape (n, d)
            First dataset of vectors, matched to second. Equal to X @ self.Q_X.

        Y_prime: np.ndarray, shape (m, d)
            Second dataset of vectors, matched to first. Equal to X @ self.Q_Y.
        """
        self.fit(X, Y)
        return self.transform(X, Y)
