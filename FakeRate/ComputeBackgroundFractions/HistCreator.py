from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg,BasicHistogramCfg

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

def removeNegativeValues2D(histo):
    for bx in xrange(histo.GetNbinsX()+2):
        for by in xrange(histo.GetNbinsY()+2):
            if histo.GetBinContent(bx,by)<0:
                histo.SetBinContent(bx,by,0)

