# # This file is part of Theano Geometry
#
# Copyright (C) 2017, Stefan Sommer (sommer@di.ku.dk)
# https://bitbucket.org/stefansommer/theanogemetry
#
# Theano Geometry is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Theano Geometry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Theano Geometry. If not, see <http://www.gnu.org/licenses/>.
#

from src.setup import *
from src.utils import *
from src.linalg import *

def initialize(M,truncate_high_order_derivatives=False):
    """ add metric related structures to manifold """

    def truncate_derivatives(e):
        if truncate_high_order_derivatives:
            return theano.gradient.disconnected_grad(e)
        else:
            return e

    d = M.dim
    x = M.element()
    u = T.matrix()

    if hasattr(M, 'g'):
        if not hasattr(M, 'gsharp'):
            M.gsharp = lambda x: T.nlinalg.matrix_inverse(M.g(x))
    elif hasattr(M, 'gsharp'):
        if not hasattr(M, 'g'):
            M.g = lambda x: T.nlinalg.matrix_inverse(M.gsharp(x))
    else:
        raise ValueError('no metric or cometric defined on manifold')
    M.gf = theano.function([x],M.g(x))
    M.gsharpf = theano.function([x],M.gsharp(x))


    M.Dg = lambda x: T.jacobian(M.g(x).flatten(),x).reshape((d,d,d)) # Derivative of metric
    M.Dgf = theano.function([x],M.Dg(x))

    ##### Measure
    M.mu_Q = lambda x: 1./T.nlinalg.Det()(M.g(x))
    M.mu_Qf = theano.function([x],M.mu_Q(x))

    ### Determinant
    M.determinant = lambda x,A: T.nlinalg.Det()(T.tensordot(M.g(x),A,(1,0)))
    M.LogAbsDeterminant = lambda x,A: LogAbsDet()(T.tensordot(M.g(x),A,(1,0)))
    A = T.matrix()
    M.Determinantf = theano.function([x,A],M.determinant(x,A))
    M.LogAbsDeterminantf = theano.function([x,A],M.LogAbsDeterminant(x,A))

    ##### Sharp and flat map:
#    M.Dgsharp = lambda q: T.jacobian(M.gsharp(q).flatten(),q).reshape((d,d,d)) # Derivative of sharp map
    v = M.vector()
    p = M.covector()
    M.flat = lambda x,v: T.dot(M.g(x),v)
    M.flatf = theano.function([x,v], M.flat(x,v))
    M.sharp = lambda x,p: T.dot(M.gsharp(x),p)
    M.sharpf = theano.function([x,p], M.sharp(x,p))

    ##### Christoffel symbols
    M.Gamma_g = lambda x: 0.5*(T.tensordot(M.gsharp(x),truncate_derivatives(M.Dg(x)),axes = [1,0])
                   +T.tensordot(M.gsharp(x),truncate_derivatives(M.Dg(x)),axes = [1,0]).dimshuffle(0,2,1)
                   -T.tensordot(M.gsharp(x),truncate_derivatives(M.Dg(x)),axes = [1,2]))
    M.Gamma_gf = theano.function([x],M.Gamma_g(x))

    # Inner Product from g
    w = M.vector()
    M.dot = lambda x,v,w: T.dot(T.dot(M.g(x),w),v)
    M.dotf = theano.function([x,v,w],M.dot(x,v,w))
    M.norm = lambda x,v: T.sqrt(M.dot(x,v,v))
    M.normf = theano.function([x,v],M.norm(x,v))
    pp = M.covector()
    M.dotsharp = lambda x,p,pp: T.dot(T.dot(M.gsharp(x),pp),p)
    M.dotsharpf = theano.function([x,p,pp],M.dotsharp(x,pp,p))
    M.conorm = lambda x,p: T.sqrt(M.dotsharp(x,p,p))
    M.conormf = theano.function([x,p],M.conorm(x,p))

    ##### Gram-Schmidt and basis
    M.gramSchmidt = lambda x,u: (GramSchmidt_f(M.dotf))(x,u)
    M.orthFrame = lambda x: T.slinalg.Cholesky()(M.gsharp(x))
    M.orthFramef = theano.function([x],M.orthFrame(x))

    ##### Hamiltonian
    q = M.element()
    p = M.covector()
    M.H = lambda q,p: 0.5*T.dot(p,T.dot(M.gsharp(q),p))
    M.Hf = theano.function([q,p],M.H(q,p))

    # gradient, divergence, and Laplace-Beltrami
    M.grad = lambda x,f: M.sharp(x,T.grad(f(x),x))
    M.div = lambda x,X: T.nlinalg.trace(T.jacobian(X(x),x))+.5*T.dot(X(x),T.grad(linalg.LogAbsDet()(M.g(x)),x))
    # M.div = lambda x,X: T.nlinalg.trace(T.jacobian(X(x),x))+T.dot(X(x),T.grad(T.log(T.sqrt(T.nlinalg.Det()(M.g(x)))),x))
    M.Laplacian = lambda x,f: M.div(x,lambda x: M.grad(x,f))
