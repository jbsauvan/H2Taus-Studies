import ROOT
from root_numpy import root2array
import statsmodels.api as sm
import numpy as np
from rootpy.plotting import Hist,Graph 
from array import array



def computeDensity(input_file, tree, var, weight=None):
    branches = [var] 
    if weight: branches.append(weight)
    data = root2array(input_file, tree, branches=branches)
    points = data.view((np.float64, len(data.dtype.names)))
    values = points[:,0] if weight else points
    weights = points[:,1] if weight else None
    print values, weights
    sumofweights = weights.sum() if weight else len(values)
    histo = Hist(25, 0, 250, type='F')
    histo.fill_array(values, weights=weights)
    fft = False if weight else True
    kde = ROOT.TKDE(len(values), array('d',values), array('d',weights))#, 0, 0, 'Binning:Unbinned')
    graph = kde.GetGraphWithErrors(500)
    for p in xrange(graph.GetN()):
        graph.SetPoint(p, graph.GetX()[p], graph.GetY()[p]*sumofweights*float(len(points))/len(values))
        graph.SetPointError(p, graph.GetEX()[p], graph.GetEY()[p]*sumofweights*float(len(points))/len(values))
    #graph.Scale(sumofweights*float(len(points))/len(values))
    #kde = sm.nonparametric.KDEUnivariate(values)
    #kde.fit(kernel='gau', bw='normal_reference', fft=fft, weights=weights)
    #graph = ROOT.TGraph(len(kde.support), kde.support, kde.density*sumofweights*float(len(points))/len(values))

    #histo.Scale(1./histo.integral(overflow=True))
    histo.Scale(float(len(points))/len(values))
    histo.Scale(1,'width')
    #graph = ROOT.TGraph(histo)
    return graph, histo

