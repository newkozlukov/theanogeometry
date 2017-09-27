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

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from pylab import rcParams
rcParams['figure.figsize'] = 9,7

from src.params import * 
from src.utils import * 

############################
#various plotting functions#
############################

def newfig(nrows=1,ncols=1,plot_number=1,new_figure=True):
    if new_figure:
        fig = plt.figure()
    else:
        fig = plt.gcf()
    ax = fig.add_subplot(nrows,ncols,plot_number,projection='3d')
    ax.set_xlim3d(-1,1), ax.set_ylim3d(-1,1), ax.set_zlim3d(-1,1)
    ax.set_aspect("equal")
    return (fig,ax)

###### plot density estimation using embedding space metric
## adapted from http://scikit-learn.org/stable/auto_examples/neighbors/plot_species_kde.html
#from sklearn.neighbors import KernelDensity
#from scipy.optimize import minimize
#from matplotlib import cm
#
#from src.metric import *
#
#def plot_density_estimate(obss_M, alpha=.2, limits=None, border=1.5, bandwidth=0.08, pts=100, cmap = cm.jet):
#        obss_q = np.array([minimize(lambda q: np.linalg.norm(Ff(q)-obs)**2,zeroU.eval()).x for obs in obss_M])
#        kde = KernelDensity(bandwidth=bandwidth, metric='pyfunc', metric_params={"func":lambda q1,q2: np.linalg.norm((Ff(q1)-Ff(q2)))},
#                        kernel='gaussian')
#        kde.fit(obss_q)
#                            
#        # grids
#        obss_q_max = np.max(obss_q,axis=0)
#        obss_q_min = np.min(obss_q,axis=0)
#        minx = limits[0] if limits is not None else obss_q_min[0]-border
#        maxx = limits[1] if limits is not None else obss_q_max[0]+border
#        miny = limits[2] if limits is not None else obss_q_min[1]-border
#        maxy = limits[3] if limits is not None else obss_q_max[1]+border
#        X, Y = np.meshgrid(np.linspace(minx,maxx,pts),np.linspace(miny,maxy,pts))
#        xy = np.vstack([Y.ravel(), X.ravel()]).T
#        xs = np.apply_along_axis(Ff,1,xy)
#        X = xs[:,0].reshape(X.shape)
#        Y = xs[:,1].reshape(X.shape)
#        Z = xs[:,2].reshape(X.shape)
#        
#        # plot
#        ax = plt.gca()
#        fs = np.exp(kde.score_samples(xy))#/np.apply_along_axis(muM_Qf,1,xy)
#        norm = mpl.colors.Normalize(vmin=0.,vmax=np.max(fs))
#        colors = cmap(norm(fs)).reshape(X.shape+(4,))
#        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cmap, facecolors = colors, linewidth=0., antialiased=True, alpha=alpha, edgecolor=(0,0,0,0), shade=False)
#        m = cm.ScalarMappable(cmap=surf.cmap,norm=norm)    
#        m.set_array(colors)
#        plt.colorbar(m, shrink=0.7)
#
##### Spherical plotting
#
## plot general function on S2
#def plot_sphere_f(f, alpha=.2, pts=100, cmap = cm.jet, parallel=False, vmin=None, colorbar=True):
#        # grids
#        phi, theta = np.meshgrid(np.linspace(0.,2.*np.pi,pts),np.linspace(0.,np.pi,pts))
#        phitheta = np.vstack([phi.ravel(), theta.ravel()]).T
#        xs = np.apply_along_axis(F_sphericalf,1,phitheta)
#        X = xs[:,0].reshape(phi.shape)
#        Y = xs[:,1].reshape(phi.shape)
#        Z = xs[:,2].reshape(phi.shape)
#        
#        # plot
#        ax = plt.gca()        
#        if not parallel:                            
#            fs = np.apply_along_axis(f,1,xs)
#        else:
#            try:
#                pf = lambda pars: (f(pars[0]),) # wrapped f for parallel execution
#                mpu.openPool()
#                sol = mpu.pool.imap(pf,mpu.inputArgs(xs,))
#                res = list(sol)
#                fs = mpu.getRes(res,0)
#            except:
#                mpu.closePool()
#                raise
#            else:
#                mpu.closePool()        
#        if vmin is None:
#            norm = mpl.colors.Normalize()
#            norm.autoscale(fs)                
#        else:
#            norm = mpl.colors.Normalize(vmin=vmin,vmax=np.max(fs))
#        colors = cmap(norm(fs)).reshape(phi.shape+(4,))
#        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cmap, facecolors = colors, linewidth=0., antialiased=True, alpha=alpha, edgecolor=(0,0,0,0), shade=False)
#        m = cm.ScalarMappable(cmap=surf.cmap,norm=norm)
#        m.set_array(colors)
#        if colorbar:
#            plt.colorbar(m, shrink=0.7)
#
## plot density estimate using spherical coordinates
#def plot_sphere_density_estimate(obss_M, alpha=.2, bandwidth=0.08, pts=100, cmap = cm.jet):
#        obss_M = np.apply_along_axis(lambda v: v/np.linalg.norm(v),1,obss_M)
#        obss_q = np.apply_along_axis(F_spherical_invf,1,obss_M)        
#        kde = KernelDensity(bandwidth=bandwidth, metric='pyfunc', metric_params={"func":lambda q1,q2: np.linalg.norm((F_sphericalf(q1)-F_sphericalf(q2)))},
#                        kernel='gaussian')
#        kde.fit(obss_q)
#                            
#        # grids
#        phi, theta = np.meshgrid(np.linspace(0.,2.*np.pi,pts),np.linspace(0.,np.pi,pts))
#        phitheta = np.vstack([phi.ravel(), theta.ravel()]).T
#        xs = np.apply_along_axis(F_sphericalf,1,phitheta)
#        X = xs[:,0].reshape(phi.shape)
#        Y = xs[:,1].reshape(phi.shape)
#        Z = xs[:,2].reshape(phi.shape)
#        
#        # plot
#        ax = plt.gca()
#        fs = np.exp(kde.score_samples(phitheta))#/np.apply_along_axis(muM_Q_sphericalf,1,phitheta)
#        norm = mpl.colors.Normalize(vmin=0.,vmax=np.max(fs))
#        colors = cmap(norm(fs)).reshape(phi.shape+(4,))
#        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cmap, facecolors = colors, linewidth=0., antialiased=True, alpha=alpha, edgecolor=(0,0,0,0), shade=False)
#        m = cm.ScalarMappable(cmap=surf.cmap,norm=norm)    
#        m.set_array(colors)
#        plt.colorbar(m, shrink=0.7)
