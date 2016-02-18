import ROOT
import Density
from array import array
import numpy as np
from root_numpy import root2array
from rootpy.plotting import Hist
import rootpy
import math


def createSmoothingWeightsFromErrors(histo):
    histoWeights = histo.Clone(histo.GetName()+"_weights")
    histoWeights.__class__ = ROOT.TH1F
    histoWeights.SetDirectory(0)
    weights = []
    for b in xrange(1,histo.GetNbinsX()+1):
        weight = 0.
        if histo.GetBinError(b)>0.:
            weight = 1./(histo.GetBinError(b)**2)
        weights.append(weight)
    sumWeights = sum(weights)
    for b in range(1,histo.GetNbinsX()+1):
        histoWeights.SetBinContent(b,weights[b-1]/sumWeights)
        histoWeights.SetBinError(b,0.)
    return histoWeights

class Smoother:
    def __init__(self):
        self.histo = None
        self.weights = None
        self.smoothHisto = None
        self.logScale = False
        self.gausWidth = 1.

    def getSmoothedValue(self, x):
        if self.logScale and x<=0.:
            raise StandardError("ERROR: use log scale and x<=0.")
        sumw = 0.
        sumwy = 0.
        nbins = self.histo.GetNbinsX()
        for b in range(1,nbins+1):
            xi = self.histo.GetXaxis().GetBinCenter(b)
            yi = self.histo.GetBinContent(b)
            if self.logScale and xi<=0.:
                raise StandardError("ERROR: use log scale and xi<=0.")
            dx = 0.
            if self.logScale:
                dx = (math.log(x) - math.log(xi))/self.gausWidth
            else:
                dx = (x-xi)/self.gausWidth
            wi = ROOT.TMath.Gaus(dx)
            if self.weights:
                wi *= self.weights.GetBinContent(b)
            sumw += wi
            sumwy += wi*yi
        value = 0.
        if sumw>0.:
            value = sumwy/sumw
        return value

    def computeSmoothHisto(self):
        if not self.histo:
            raise StandardError("ERROR: non existing input histo")
        self.smoothHisto = self.histo.Clone(self.histo.GetName()+"_smooth")
        self.smoothHisto.__class__ = ROOT.TH1D
        self.smoothHisto.SetDirectory(0)
        nbins = self.smoothHisto.GetNbinsX()
        for b in range(1,nbins+1):
            x = self.smoothHisto.GetBinCenter(b)
            smoothedValue = self.getSmoothedValue(x)
            self.smoothHisto.SetBinContent(b,smoothedValue)

    def getContinuousSmoothHisto(self):
        if not self.histo:
            raise StandardError("ERROR: non existing input histo")
        mini = self.histo.GetXaxis().GetBinLowEdge(1)
        maxi = self.histo.GetXaxis().GetBinUpEdge(self.histo.GetNbinsX())
        if self.logScale and mini<0.:
            raise StandardError("ERROR: use log scale and min value<0")
        if mini==0.:
            mini = self.histo.GetXaxis().GetBinUpEdge(1)/10.
        nbins = 1000
        bins = []
        if self.logScale:
            dx = (math.log(maxi) - math.log(mini))/nbins
            bins = [math.exp(math.log(mini)+i*dx) for i in range(0,nbins+1)]
        else:
            dx = (maxi - mini)/nbins
            bins = [mini+i*dx for i in range(0,nbins+1)]
        smoothHisto = ROOT.TH1D(self.histo.GetName()+"_cont",self.histo.GetTitle(), nbins, array('f',bins))
        for b in range(1,nbins+1):
            x = smoothHisto.GetBinCenter(b)
            smoothedValue = self.getSmoothedValue(x)
            smoothHisto.SetBinContent(b,smoothedValue)
        return smoothHisto




class Closure:
    def __init__(self):
        self.data = {}

    def fillData(self, name, input_file, tree, var, weight=None):
        branches = [var] 
        if weight: branches.append(weight)
        data = root2array(input_file, tree, branches=branches)
        points = data.view((np.float64, len(data.dtype.names)))
        values = points[:,0] if weight else points
        weights = points[:,1] if weight else None
        if not name in self.data: self.data[name] = {}
        self.data[name]['Data'] = [values, weights]

    def clearData(self, name=None):
        if name:
            self.data[name]['Data'] = None
        else:
            for data in self.data.values():
                data['Data'] = None


    def computeTKDE(self, name):
        if not name in self.data or not 'Data' in self.data[name]:
            raise StandardError('Cannot find data for {NAME}'.format(NAME=name))
        values = self.data[name]['Data'][0]
        weights = self.data[name]['Data'][1]
        sumofweights = weights.sum() if isinstance(weights,np.ndarray) else len(values)
        kde = ROOT.TKDE(len(values), array('d',values), array('d',weights)) if isinstance(weights,np.ndarray) else ROOT.TKDE(len(values), array('d',values))
        graph = kde.GetGraphWithErrors(500)
        for p in xrange(graph.GetN()):
            graph.SetPoint(p, graph.GetX()[p], graph.GetY()[p]*sumofweights)
            graph.SetPointError(p, graph.GetEX()[p], graph.GetEY()[p]*sumofweights)
        self.data[name]['TKDE'] = graph

    def computeHisto(self, name):
        if not name in self.data or not 'Data' in self.data[name]:
            raise StandardError('Cannot find data for {NAME}'.format(NAME=name))
        values = self.data[name]['Data'][0]
        weights = self.data[name]['Data'][1]
        histo = Hist(25, 0, 250, type='F')
        histo.fill_array(values, weights=weights)
        histo.Scale(1,'width')
        self.data[name]['Histo'] = histo

    def computeDiff(self, name1, name2, type, smoothWidth=0.2, smoothLog=True):
        if not name1 in self.data or not type in self.data[name1]:
            raise StandardError('Cannot find {TYPE} for {NAME}'.format(TYPE=type,NAME=name1))
        if not name2 in self.data or not type in self.data[name2]:
            raise StandardError('Cannot find {TYPE} for {NAME}'.format(TYPE=type,NAME=name2))
        if isinstance(self.data[name1][type], ROOT.TGraphErrors):
            graph1 = self.data[name1][type]
            graph2 = self.data[name2][type]
            xs1 = graph1.GetX()
            xs2 = graph2.GetX()
            xs1.SetSize(graph1.GetN())
            xs2.SetSize(graph2.GetN())
            xs = list(xs1) + list(xs2)
            xs.sort()
            ys1 = [graph1.Eval(x) for x in xs]
            ys2 = [graph2.Eval(x) for x in xs]
            ysdiff = [y2-y1 for y1,y2 in zip(ys1,ys2)]
            graphdiff = ROOT.TGraph(len(xs), array('f',xs), array('f',ysdiff))
            if not'{1}-{0}'.format(name1,name2) in self.data: self.data['{1}-{0}'.format(name1,name2)] = {}
            self.data['{1}-{0}'.format(name1,name2)][type] = graphdiff
        elif isinstance(self.data[name1][type], ROOT.TH1F):
            histo1 = self.data[name1][type]
            histo2 = self.data[name2][type]
            histodiff = histo2 - histo1
            if not'{1}-{0}'.format(name1,name2) in self.data: self.data['{1}-{0}'.format(name1,name2)] = {}
            self.data['{1}-{0}'.format(name1,name2)][type] = histodiff
            ## Smooth diff histo
            smoother = Smoother()
            smoother.logScale = smoothLog
            smoother.gausWidth = smoothWidth
            smoother.histo = histodiff
            smoother.weights = createSmoothingWeightsFromErrors(histodiff)
            smoother.computeSmoothHisto()
            self.data['{1}-{0}'.format(name1,name2)][type+'_Smooth'] = smoother.getContinuousSmoothHisto()

    def computeRatio(self, name1, name2, type, smoothWidth=0.2, smoothLog=True):
        if not name1 in self.data or not type in self.data[name1]:
            raise StandardError('Cannot find {TYPE} for {NAME}'.format(TYPE=type,NAME=name1))
        if not name2 in self.data or not type in self.data[name2]:
            raise StandardError('Cannot find {TYPE} for {NAME}'.format(TYPE=type,NAME=name2))
        if isinstance(self.data[name1][type], ROOT.TGraphErrors):
            # Find point above which there are 50 events 
            # FIXME: make it configurable
            cut1 = np.percentile(self.data[name1]['Data'][0], (len(self.data[name1]['Data'][0])-50.)/len(self.data[name1]['Data'][0])*100.)
            cut2 = np.percentile(self.data[name2]['Data'][0], (len(self.data[name2]['Data'][0])-50.)/len(self.data[name2]['Data'][0])*100.)
            cut = min(cut1,cut2)
            graph1 = self.data[name1][type]
            graph2 = self.data[name2][type]
            xs1 = graph1.GetX()
            xs2 = graph2.GetX()
            xs1.SetSize(graph1.GetN())
            xs2.SetSize(graph2.GetN())
            xs = list(xs1) + list(xs2)
            xs.sort()
            ys1 = [graph1.Eval(min(x,cut)) for x in xs]
            ys2 = [graph2.Eval(min(x,cut)) for x in xs]
            errors = [0]*len(xs)
            ysratio = [y2/y1 if y1!=0 else 1. for y1,y2 in zip(ys1,ys2)]
            graphratio = ROOT.TGraphAsymmErrors(len(xs), array('f',xs), array('f',ysratio), array('f',errors), array('f',errors), array('f',errors), array('f',errors))
            if not'{1}/{0}'.format(name1,name2) in self.data: self.data['{1}/{0}'.format(name1,name2)] = {}
            self.data['{1}/{0}'.format(name1,name2)][type] = graphratio
        elif isinstance(self.data[name1][type], ROOT.TH1F):
            histo1 = self.data[name1][type]
            histo2 = self.data[name2][type]
            historatio = histo2 / histo1
            if not'{1}/{0}'.format(name1,name2) in self.data: self.data['{1}/{0}'.format(name1,name2)] = {}
            self.data['{1}/{0}'.format(name1,name2)][type] = historatio
            ## Smooth ratio histo
            smoother = Smoother()
            smoother.logScale = smoothLog
            smoother.gausWidth = smoothWidth
            smoother.histo = historatio
            smoother.weights = createSmoothingWeightsFromErrors(historatio)
            smoother.computeSmoothHisto()
            self.data['{1}/{0}'.format(name1,name2)][type+'_Smooth'] = smoother.getContinuousSmoothHisto()




