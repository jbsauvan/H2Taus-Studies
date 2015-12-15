import ROOT
import sys
import os


class Config:
    def __init__(self):
        self.color = ROOT.kBlack
        self.markerStyle = 20
        self.lineStyle = 1
        self.lineWidth = 2
        self.binWidthScaling = False
        self.unitScaling = False
        self.xTitle = ""
        self.yTitle = ""
        self.legend = ""
        self.plotCfg = ""

    def apply(self, histo):
        histo.SetMarkerColor(self.color)
        histo.SetLineColor(self.color)
        histo.SetMarkerStyle(self.markerStyle)
        histo.SetLineStyle(self.lineStyle)
        histo.SetLineWidth(self.lineWidth)
        histo.SetXTitle(self.xTitle)
        histo.SetYTitle(self.yTitle)
        if self.unitScaling: histo.Scale(1./histo.GetSumOfWeights())
        if self.binWidthScaling: self.applyBinWidthScaling(histo)

    def applyBinWidthScaling(self, histo):
        nbins = histo.GetNbinsX()
        for b in xrange(1,nbins+1):
            width = histo.GetBinWidth(b)
            content = histo.GetBinContent(b)
            error = histo.GetBinError(b)
            histo.SetBinContent(b, content/width)
            histo.SetBinError(b, error/width)


class ComparisonPlot:
    def __init__(self):
        self.setPlotStyle()
        self.name = "plot"
        self.plotDir = "plots/"
        self.logy = False
        self.legendPosition = [0.5, 0.7, 0.95, 0.9]
        self.histos = []


    def addHisto(self, fileName, histoName, config):
        file = ROOT.TFile.Open(fileName)
        if not file: raise StandardError("Cannot open file "+fileName)
        histo = file.Get(histoName)
        if not histo: raise StandardError("Cannot load histogram "+histoName+" from file "+fileName)
        histo.__class__ = ROOT.TH1F
        histo.SetDirectory(0)
        if len(self.histos)>0: config.plotCfg += " same"
        self.histos.append( (histo, config) )
        file.Close()

    def plot(self):
        if not os.path.exists(self.plotDir):
            os.makedirs(self.plotDir)
        self.setPlotStyle()
        canvas = ROOT.TCanvas("c_"+self.name, self.name, 800, 800)
        maximum = 0.
        minimum = sys.float_info.max
        for histo,config in self.histos:
            config.apply(histo)
            if histo.GetMaximum()>maximum: maximum = histo.GetMaximum()
            if histo.GetMinimum()<minimum and histo.GetMinimum()>0.: minimum = histo.GetMinimum()
        for histo,config in self.histos:
            if not self.logy: histo.SetAxisRange(0., maximum*1.1, "Y")
            else: histo.SetAxisRange(minimum*0.9, maximum*1.1, "Y")
            histo.Draw(config.plotCfg)
        if self.logy: canvas.SetLogy()
        legend = ROOT.TLegend(self.legendPosition[0],self.legendPosition[1],self.legendPosition[2],self.legendPosition[3])
        legend.SetFillColor(0)
        legend.SetLineWidth(0)
        legend.SetLineColor(0)
        for histo, config in self.histos:
            legendCfg = "lp"
            if "HIST" in config.plotCfg or "hist" in config.plotCfg: legendCfg = "l"
            legend.AddEntry(histo, config.legend, legendCfg)
        legend.Draw()
        canvas.Print(self.plotDir+"/"+self.name+".png")
        canvas.Print(self.plotDir+"/"+self.name+".eps")
        canvas.Print(self.plotDir+"/"+self.name+".pdf")
        canvas.Print(self.plotDir+"/"+self.name+".C")


    def setPlotStyle(self):
        ROOT.gROOT.SetStyle("Plain")
        ROOT.gStyle.SetOptStat()
        ROOT.gStyle.SetOptFit(0)
        ROOT.gStyle.SetOptTitle(0)
        ROOT.gStyle.SetFrameLineWidth(1)
        ROOT.gStyle.SetPadBottomMargin(0.13)
        ROOT.gStyle.SetPadLeftMargin(0.13)
        ROOT.gStyle.SetPadTopMargin(0.05)
        ROOT.gStyle.SetPadRightMargin(0.03)

        ROOT.gStyle.SetLabelFont(42,"X")
        ROOT.gStyle.SetLabelFont(42,"Y")
        ROOT.gStyle.SetLabelSize(0.04,"X")
        ROOT.gStyle.SetLabelSize(0.04,"Y")
        ROOT.gStyle.SetLabelOffset(0.01,"Y")
        ROOT.gStyle.SetTickLength(0.03,"X")
        ROOT.gStyle.SetTickLength(0.03,"Y")
        ROOT.gStyle.SetLineWidth(1)
        ROOT.gStyle.SetTickLength(0.04 ,"Z")

        ROOT.gStyle.SetTitleSize(0.1)
        ROOT.gStyle.SetTitleFont(42,"X")
        ROOT.gStyle.SetTitleFont(42,"Y")
        ROOT.gStyle.SetTitleSize(0.07,"X")
        ROOT.gStyle.SetTitleSize(0.07,"Y")
        ROOT.gStyle.SetTitleOffset(0.8,"X")
        ROOT.gStyle.SetTitleOffset(0.9,"Y")
        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetPalette(1)
        ROOT.gStyle.SetPaintTextFormat("3.2f")
        ROOT.gROOT.ForceStyle()



