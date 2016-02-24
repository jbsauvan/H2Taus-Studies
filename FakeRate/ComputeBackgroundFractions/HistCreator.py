from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg,BasicHistogramCfg
import numpy as np
from ROOT import TH1F, TFile, gROOT

class HistoStack:
    def __init__(self, name):
        self.name = name
        self.histos = {}
        self.histo_sum = None

    def update(self, stack):
        self.histos.update(stack.histos)

    def Add(self, name, histo):
        if not name in self.histos:
            self.histos[name] = histo.Clone(self.name+'_'+histo.GetName())
        else:
            self.histos[name].Add(histo)
    def Sum(self):
        if not self.histo_sum:
            for histo in self.histos.values():
                if not self.histo_sum:
                    self.histo_sum = histo.Clone(self.name+'_sum')
                else:
                    self.histo_sum.Add(histo)
        return self.histo_sum


def createHistograms(hist_cfg):
    histos = HistoStack(hist_cfg.name)
    for cfg in hist_cfg.cfgs:
        # First check whether it's a sub-histo or not
        if isinstance(cfg, HistogramCfg):
            histos.Add(cfg.name, createHistograms(cfg).Sum())
        elif isinstance(cfg, BasicHistogramCfg):
            print "Opening file", cfg.histo_file_name
            histo_file = TFile.Open(cfg.histo_file_name)
            print "Retrieving histo", cfg.histo_name
            hist = histo_file.Get(cfg.histo_name)
            hist.__class__ = TH1F
            hist.SetDirectory(0)
            hist.SetName(cfg.name+'_'+hist.GetName())
            histo_file.Close()
            gROOT.cd()
            #
            hist.Scale(cfg.scale)
            if not cfg.is_data:
                hist.Scale(hist_cfg.lumi*cfg.xsec/cfg.sumweights) 
            histos.Add(cfg.name, hist)
    return histos

def create2DHistograms(hist_cfg):
    histos = HistoStack(hist_cfg.name)
    for cfg in hist_cfg.cfgs:
        # First check whether it's a sub-histo or not
        if isinstance(cfg, HistogramCfg):
            histos.Add(cfg.name, createHistograms(cfg).Sum())
        elif isinstance(cfg, BasicHistogramCfg):
            print "Opening file", cfg.histo_file_name
            histo_file = TFile.Open(cfg.histo_file_name)
            print "Retrieving histo", cfg.histo_name
            hist = histo_file.Get(cfg.histo_name)
            hist.__class__ = TH2F
            hist.SetDirectory(0)
            hist.SetName(cfg.name+'_'+hist.GetName())
            histo_file.Close()
            gROOT.cd()
            #
            hist.Scale(cfg.scale)
            if not cfg.is_data:
                hist.Scale(hist_cfg.lumi*cfg.xsec/cfg.sumweights) 
            histos.Add(cfg.name, hist)
    return histos

def removeNegativeValues(histo):
    for b in xrange(histo.GetNbinsX()+2):
        if histo.GetBinContent(b)<0:
            histo.SetBinContent(b,0)
            histo.SetBinError(b,abs(histo.GetBinContent(b)))

def removeNegativeValues2D(histo):
    for bx in xrange(histo.GetNbinsX()+2):
        for by in xrange(histo.GetNbinsY()+2):
            if histo.GetBinContent(bx,by)<0:
                histo.SetBinContent(bx,by,0)
                histo.SetBinError(bx,by,abs(histo.GetBinContent(bx,by)))

def checkFractionSums2D(histos):
    nbinsx = histos[0].GetNbinsX()
    nbinsy = histos[0].GetNbinsY()
    for bx in xrange(1, nbinsx+1):
        for by in xrange(1, nbinsy+1):
            binsum = sum([h.GetBinContent(bx,by) for h in histos])
            if binsum==0:
                # Take local average fraction (from neighbour bins) for each histo
                for histo in histos:
                    neighbours = []
                    for ix in [-1,0,1]:
                        shiftx = bx+ix
                        if shiftx<1 or shiftx>nbinsx: continue
                        for iy in [-1,0,1]:
                            if ix==0 and iy==0: continue
                            shifty = by+iy
                            if shifty<1 or shifty>nbinsy: continue
                            neighbour = histo.GetBinContent(shiftx,shifty)
                            neighbours.append(neighbour)
                    mean = np.mean(neighbours) # Simple mean, errors not taken into account
                    histo.SetBinContent(bx,by,mean)
                    histo.SetBinError(bx,by,mean)
                # Correct if new sum is not equal to 1
                newsum = sum([h.GetBinContent(bx,by) for h in histos])
                for histo in histos:
                    content = histo.GetBinContent(bx,by)
                    histo.SetBinContent(bx,by,content/newsum)
                    histo.SetBinError(bx,by,content/newsum)
            elif abs(binsum-1)>1.e-5:
                print 'Warning: fraction sum is equal to',binsum,'in bin', bx, by


