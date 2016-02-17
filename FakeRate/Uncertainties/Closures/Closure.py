import ROOT
import Density
from array import array
import numpy as np
from root_numpy import root2array
from rootpy.plotting import Hist
import rootpy


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

    def computeDiff(self, name1, name2, type):
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

    def computeRatio(self, name1, name2, type):
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
            histodiff = histo2 / histo1
            if not'{1}/{0}'.format(name1,name2) in self.data: self.data['{1}/{0}'.format(name1,name2)] = {}
            self.data['{1}/{0}'.format(name1,name2)][type] = histodiff



