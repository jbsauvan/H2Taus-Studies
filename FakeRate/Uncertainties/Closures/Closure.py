import ROOT
import Density
from array import array
import numpy as np
from root_numpy import root2array
from rootpy.plotting import Hist, Canvas
import rootpy
import math
import copy



def weighted_quantile(values, quantiles, sample_weight=None, values_sorted=False, old_style=False):
    """ Very close to numpy.percentile, but supports weights.
    NOTE: quantiles should be in [0, 1]!
    :param values: numpy.array with data
    :param quantiles: array-like with many quantiles needed
    :param sample_weight: array-like of the same length as `array`
    :param values_sorted: bool, if True, then will avoid sorting of initial array
    :param old_style: if True, will correct output to be consistent with numpy.percentile.
    :return: numpy.array with computed quantiles.
    """
    #values = np.array(values)
    quantiles = np.array(quantiles)
    if sample_weight is None:
        sample_weight = np.ones(len(values))
    #sample_weight = np.array(sample_weight)
    assert np.all(quantiles >= 0) and np.all(quantiles <= 1), 'quantiles should be in [0, 1]'

    if not values_sorted:
        sorter = np.argsort(values)
        values = values[sorter]
        sample_weight = sample_weight[sorter]

    weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight
    if old_style:
        # To be convenient with numpy.percentile
        weighted_quantiles -= weighted_quantiles[0]
        weighted_quantiles /= weighted_quantiles[-1]
    else:
        weighted_quantiles /= np.sum(sample_weight)
    return np.interp(quantiles, weighted_quantiles, values)

#def createSmoothingWeightsFromErrors(histo1, histo2):
    #histoWeights = histo1.Clone(histo1.GetName()+"_weights")
    #histoWeights.__class__ = ROOT.TH1F
    #histoWeights.SetDirectory(0)
    #weights = []
    #for b in xrange(1,histo1.GetNbinsX()+1):
        #weight = 0.
        #relerr1 = histo1.GetBinError(b)/histo1.GetBinContent(b) if histo1.GetBinContent(b)>0. else 1.
        #relerr2 = histo2.GetBinError(b)/histo2.GetBinContent(b) if histo2.GetBinContent(b)>0. else 1.
        #weight = 1./(max(relerr1, relerr2)**2)
        #weights.append(weight)
    #sumWeights = sum(weights)
    #for b in range(1,histo1.GetNbinsX()+1):
        #histoWeights.SetBinContent(b,weights[b-1]/sumWeights)
        #histoWeights.SetBinError(b,0.)
    #return histoWeights

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
        self.rescaling = lambda x:x
        self.invertRescaling = self.rescaling
        self.gausWidth = 1.
        self.doErrors = False
        self.random = ROOT.TRandom3()


    def fluctuateHisto(self):
        histoRnd = self.histo.Clone(self.histo.GetName()+'_rnd')
        nbins = self.histo.GetNbinsX()
        for b in range(1,nbins+1):
            content = self.histo.GetBinContent(b)
            error = self.histo.GetBinError(b)
            newcontent = self.random.Gaus(content,error)
            histoRnd.SetBinContent(b,newcontent)
        return histoRnd


    def getSmoothedValue(self, x):
        sumw = 0.
        sumwy = 0.
        nbins = self.histo.GetNbinsX()
        for b in range(1,nbins+1):
            xi = self.histo.GetXaxis().GetBinCenter(b)
            yi = self.histo.GetBinContent(b)
            dx = 0.
            dx = (self.rescaling(x)-self.rescaling(xi))/self.gausWidth
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
        if mini==0.:
            mini = self.histo.GetXaxis().GetBinUpEdge(1)/10.
        nbins = 500
        bins = []
        #dx = (maxi - mini)/nbins
        #bins = [mini+i*dx for i in range(0,nbins+1)]
        dx = (self.rescaling(maxi) - self.rescaling(mini))/nbins
        bins = [self.invertRescaling(self.rescaling(mini)+i*dx) for i in range(0,nbins+2)]
        xs = [(x1+x2)/2 for x1,x2 in zip(bins[:-1],bins[1:])]
        ys = [self.getSmoothedValue(x) for x in xs]
        smoothGraph = ROOT.TGraphAsymmErrors(len(xs), array('f',xs), array('f',ys), array('f',[0]*len(xs)), array('f',[0]*len(xs)), array('f',[0]*len(xs)), array('f',[0]*len(xs)))
        ysRnds = None
        if self.doErrors:
            for i in xrange(100):
                histoNom = self.histo
                self.histo = self.fluctuateHisto()
                ysRnd = [self.getSmoothedValue(x) for x in xs]
                if not ysRnds: 
                    ysRnds = [[y] for y in ysRnd]
                else:
                    ysRnds = [yy+[y] for yy,y in zip(ysRnds,ysRnd)]
                self.histo.Delete()
                self.histo = histoNom
            ysRMS = [np.std(yy) for yy in ysRnds]
            ysUp = [y+rms for y,rms in zip(ys,ysRMS)]
            ysDown = [y-rms for y,rms in zip(ys,ysRMS)]
            ysDown.reverse()
            ysUpDown = ysUp + ysDown
            xsreversed = copy.deepcopy(xs)
            xsreversed.reverse()
            xsdouble = xs + xsreversed
            smoothErrorGraph = ROOT.TGraphAsymmErrors(len(xsdouble), array('f',xsdouble), array('f',ysUpDown), array('f',[0]*len(xsdouble)), array('f',[0]*len(xsdouble)), array('f',[0]*len(xsdouble)), array('f',[0]*len(xsdouble)))
        else:
            xsreversed = copy.deepcopy(xs)
            xsreversed.reverse()
            xsdouble = xs + xsreversed
            ysreversed = copy.deepcopy(ys)
            ysreversed.reverse()
            ysdouble = ys + ysreversed
            smoothErrorGraph = ROOT.TGraphAsymmErrors(len(xsdouble), array('f',xsdouble), array('f',ysdouble), array('f',[0]*len(xsdouble)), array('f',[0]*len(xsdouble)), array('f',[0]*len(xsdouble)), array('f',[0]*len(xsdouble)))
        return smoothGraph,smoothErrorGraph




class Closure:
    def __init__(self):
        self.weights = False
        self.data = {}

    def fillData(self, name, input_files, tree, var, weight=None, global_weights=None):
        all_points = None
        for input_file,global_weight in zip(input_files,global_weights):
            branches = [var] 
            total_weight = copy.copy(weight) if weight else '1'
            if global_weight!=1:
                total_weight += '*{}'.format(global_weight)
            if total_weight!=1:
                branches.append(total_weight)
                self.weights = True
            data = root2array(input_file, tree, branches=branches)
            points = data.view((np.float64, len(data.dtype.names)))
            if all_points==None: all_points = points
            else: all_points = np.vstack((all_points, points))
        values = all_points[:,0] if self.weights else points
        weights = all_points[:,1] if self.weights else None
        if not name in self.data: self.data[name] = {}
        self.data[name]['Data'] = [values, weights]

    def clearData(self, name=None):
        if name:
            self.data[name]['Data'] = None
        else:
            for data in self.data.values():
                data['Data'] = None


    def computeTKDE(self, name, min=1., max=0.):
        if not name in self.data or not 'Data' in self.data[name]:
            raise StandardError('Cannot find data for {NAME}'.format(NAME=name))
        values = self.data[name]['Data'][0]
        weights = self.data[name]['Data'][1]
        sumofweights = weights.sum() if isinstance(weights,np.ndarray) else len(values)
        kde = ROOT.TKDE(len(values), array('d',values), array('d',weights)) if isinstance(weights,np.ndarray) else ROOT.TKDE(len(values), array('d',values))
        graph = kde.GetGraphWithErrors(500, min, max)
        for p in xrange(graph.GetN()):
            graph.SetPoint(p, graph.GetX()[p], graph.GetY()[p]*sumofweights)
            graph.SetPointError(p, graph.GetEX()[p], graph.GetEY()[p]*sumofweights)
        self.data[name]['TKDE'] = graph

    def computeCDF(self, name):
        if not name in self.data or not 'Data' in self.data[name]:
            raise StandardError('Cannot find data for {NAME}'.format(NAME=name))
        values = self.data[name]['Data'][0]
        weights = self.data[name]['Data'][1]
        quantiles = weighted_quantile(values, np.arange(0.,1.01,0.01), weights)
        graph = ROOT.TGraph(quantiles.size, quantiles, np.arange(0.,1.01,0.01))
        invertgraph = ROOT.TGraph(quantiles.size, np.arange(0.,1.01,0.01), quantiles)
        self.data[name]['CDF'] = graph
        self.data[name]['CDFInvert'] = invertgraph



    def computeHisto(self, name, bins):
        if not name in self.data or not 'Data' in self.data[name]:
            raise StandardError('Cannot find data for {NAME}'.format(NAME=name))
        values = self.data[name]['Data'][0]
        weights = self.data[name]['Data'][1]
        histo = Hist(bins, type='F')
        histo.Sumw2()
        histo.fill_array(values, weights=weights)
        histo.Scale(1,'width')
        #self.data[name]['Histo'] = histo
        self.data[name]['Histo_'+str(hash(str(bins)))] = histo

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
            smoother.gausWidth = smoothWidth
            smoother.histo = histodiff
            smoother.weights = createSmoothingWeightsFromErrors(histodiff)
            #smoother.weights = createSmoothingWeightsFromErrors(histo1,histo2)
            #smoother.computeSmoothHisto()
            self.data['{1}-{0}'.format(name1,name2)][type+'_Smooth'] = smoother.getContinuousSmoothHisto()[0]

    def computeRatio(self, name1, name2, type, smoothWidth=0.2, kernelDistance='Adapt', doErrors=False):
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
            smoother.gausWidth = smoothWidth
            smoother.histo = historatio
            smoother.doErrors = doErrors
            if kernelDistance is 'Adapt':
                cdf = self.data[name2]['CDF']
                icdf = self.data[name2]['CDFInvert']
                smoother.rescaling = lambda x : cdf.Eval(x)
                smoother.invertRescaling = lambda x : icdf.Eval(x)
            elif kernelDistance is 'Linear':
                smoother.rescaling = lambda x : x
                smoother.invertRescaling = lambda x : x
            elif kernelDistance is 'Log':
                smoother.rescaling = lambda x : math.log(x)
                smoother.invertRescaling = lambda x : math.exp(x)
            smoother.weights = createSmoothingWeightsFromErrors(historatio)
            #smoother.weights = createSmoothingWeightsFromErrors(histo1,histo2)
            #smoother.computeSmoothHisto()
            self.data['{1}/{0}'.format(name1,name2)][type+'_Smooth'] = smoother.getContinuousSmoothHisto()[0]
            self.data['{1}/{0}'.format(name1,name2)][type+'_SmoothError'] = smoother.getContinuousSmoothHisto()[1]



def plotClosure(name, closure, bins, smoothWidth=0.1, kernelDistance='Adapt', doErrors=False):
    binid = hash(str(bins))
    closure.computeHisto('True', bins)
    closure.computeHisto('Est', bins)
    closure.computeRatio('Est', 'True', 'Histo_{H}'.format(H=binid), smoothWidth, kernelDistance, doErrors)
    #
    histoTrue = closure.data['True']['Histo_{H}'.format(H=binid)]
    histoEst  = closure.data['Est']['Histo_{H}'.format(H=binid)]
    histoRatio = closure.data['True/Est']['Histo_{H}'.format(H=binid)]
    histoSmoothRatio = closure.data['True/Est']['Histo_{H}_Smooth'.format(H=binid)]
    histoSmoothRatioError = closure.data['True/Est']['Histo_{H}_SmoothError'.format(H=binid)]
    #
    ############ plot raw distributions
    histoDummy = Hist(1, bins[0],  bins[-1], type='F')
    values = []
    values.append(histoTrue.GetMaximum())
    values.append(histoTrue.GetMinimum())
    values.append(histoEst.GetMaximum())
    values.append(histoEst.GetMinimum())
    maxi = max(values)*1.1
    mini = min(values)
    histoDummy.SetAxisRange(mini, maxi, 'Y')
    ##
    histoTrue.SetMarkerColor(ROOT.kBlack)
    histoEst.SetMarkerStyle(24)
    histoEst.SetMarkerColor(ROOT.kGray+3)
    ##
    canvas = Canvas(800, 800)
    canvas.SetName('{NAME}_Canvas'.format(NAME=name))
    histoDummy.SetXTitle('m_{vis} [GeV]')
    histoDummy.SetYTitle('Events')
    histoDummy.Draw()
    histoTrue.Draw('same')
    histoEst.Draw('same')
    legend = ROOT.TLegend(0.4,0.7,0.9,0.9)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.AddEntry(histoTrue, 'True background', 'lp')
    legend.AddEntry(histoEst, 'Estimated background', 'lp')
    legend.Draw()
    canvas.Print('results/{NAME}_NonClosure.png'.format(NAME=name))


    ################ Plot ratios
    histoDummyRatio = Hist(1, bins[0],  bins[-1], type='F')
    values = []
    values.append(histoRatio.GetMaximum())
    values.append(histoRatio.GetMinimum())
    maxi = max(values)
    mini = min(values)
    maxi = maxi*1.1 if maxi>0 else maxi*0.9
    mini = mini*1.1 if mini<0 else mini*0.9
    histoDummyRatio.SetAxisRange(mini, maxi, 'Y')
    ##
    histoRatio.SetMarkerColor(ROOT.kBlack)
    histoSmoothRatio.SetLineColor(ROOT.kGray+3)
    histoSmoothRatio.SetLineWidth(2)
    histoSmoothRatioError.SetLineColor(ROOT.kGray+1)
    histoSmoothRatioError.SetFillColor(ROOT.kGray+1)
    ##
    canvasRatio = Canvas(800, 800)
    canvasRatio.SetName('{NAME}_Ratio_Canvas'.format(NAME=name))
    histoDummyRatio.SetXTitle('m_{vis} [GeV]')
    histoDummyRatio.SetYTitle('Ratio')
    histoDummyRatio.Draw()
    histoSmoothRatioError.Draw('fl same')
    histoSmoothRatio.Draw('pl same')
    histoRatio.Draw('same')
    canvasRatio.Print('results/{NAME}_NonClosure_Ratio.png'.format(NAME=name))

def plotSummary(name, closure, xmin=0, xmax=1):
    histoSmoothRatios = []
    for hname,graph in closure.data['True/Est'].items():
        if 'Histo' in hname and 'Smooth' in hname and not 'Error' in hname:
            histoSmoothRatios.append(graph)
    ################ Plot ratios
    histoDummyRatio = Hist(1, xmin,  xmax, type='F')
    values = []
    for ratio in histoSmoothRatios:
        for p in xrange(ratio.GetN()):
            values.append(ratio.GetY()[p])
    maxi = max(values)
    mini = min(values)
    maxi = maxi*1.1 if maxi>0 else maxi*0.9
    mini = mini*1.1 if mini<0 else mini*0.9
    histoDummyRatio.SetAxisRange(mini, maxi, 'Y')
    ##
    for ratio in histoSmoothRatios:
        ratio.SetLineColor(ROOT.kGray+3)
        ratio.SetLineWidth(1)
    ##
    canvasRatio = Canvas(800, 800)
    canvasRatio.SetName('Ratio_Summary_Canvas')
    histoDummyRatio.SetXTitle('m_{vis} [GeV]')
    histoDummyRatio.SetYTitle('Ratio')
    histoDummyRatio.Draw()
    for ratio in histoSmoothRatios:
        ratio.Draw('l same')
    canvasRatio.Print('results/{NAME}_NonClosure_Ratio_Summary.png'.format(NAME=name))

