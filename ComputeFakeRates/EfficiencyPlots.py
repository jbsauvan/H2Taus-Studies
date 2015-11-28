import ROOT
import os


def setPlotStyle():
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetOptStat()
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetFrameLineWidth(1)
    ROOT.gStyle.SetPadBottomMargin(0.13)
    ROOT.gStyle.SetPadLeftMargin(0.15)
    ROOT.gStyle.SetPadTopMargin(0.03)
    ROOT.gStyle.SetPadRightMargin(0.03)

    ROOT.gStyle.SetLabelFont(42,"X")
    ROOT.gStyle.SetLabelFont(42,"Y")
    ROOT.gStyle.SetLabelSize(0.05,"X")
    ROOT.gStyle.SetLabelSize(0.05,"Y")
    ROOT.gStyle.SetLabelOffset(0.01,"Y")
    ROOT.gStyle.SetTickLength(0.04,"X")
    ROOT.gStyle.SetTickLength(0.04,"Y")
    ROOT.gStyle.SetLineWidth(1)
    ROOT.gStyle.SetTickLength(0.04 ,"Z")

    ROOT.gStyle.SetTitleSize(0.1)
    ROOT.gStyle.SetTitleFont(42,"X")
    ROOT.gStyle.SetTitleFont(42,"Y")
    ROOT.gStyle.SetTitleSize(0.05,"X")
    ROOT.gStyle.SetTitleSize(0.05,"Y")
    ROOT.gStyle.SetTitleOffset(1.1,"X")
    ROOT.gStyle.SetTitleOffset(1.5,"Y")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetPaintTextFormat("3.2f")
    ROOT.gROOT.ForceStyle()

class PlotInfo:
    def __init__(self):
        self.markerStyle = 20
        self.markerColor = ROOT.kBlack
        self.lineColor = ROOT.kBlack
        self.xTitle = ""
        self.yTitle = ""


class EfficiencyPlot:
    def __init__(self):
        self.name = "efficiency"
        self.plotDir = "plots/"
        self.passHistos = []
        self.totalHistos = []
        self.efficiencyGraphs = []
        self.canvas = None
        self.plotInfos = []

    def efficiency(self, pas, total, option, plotInfo):
        self.passHistos.append(pas)
        self.totalHistos.append(total)
        self.efficiencyGraphs.append(ROOT.TGraphAsymmErrors())
        self.efficiencyGraphs[-1].Divide(pas,total, option) 
        self.efficiencyGraphs[-1].SetMarkerStyle(plotInfo.markerStyle)
        self.efficiencyGraphs[-1].SetMarkerColor(plotInfo.markerColor)
        self.efficiencyGraphs[-1].SetLineColor(plotInfo.lineColor)
        self.plotInfos.append(plotInfo)

    def plot(self, minEff=0.95, maxEff=1.01):
        setPlotStyle()
        if not os.path.exists(self.plotDir):
            os.makedirs(self.plotDir)
        np = self.efficiencyGraphs[-1].GetN()
        xMin = self.totalHistos[-1].GetXaxis().GetBinLowEdge(1)
        xMax = self.totalHistos[-1].GetXaxis().GetBinUpEdge(self.totalHistos[-1].GetNbinsX())
        self.canvas = ROOT.TCanvas("c_"+self.name, "c_"+self.name, 800, 800)
        self.canvas.SetGrid()

        hDummy = ROOT.TH1F("hDummy", "dummy", 1, xMin, xMax)
        hDummy.SetXTitle(self.plotInfos[-1].xTitle)
        hDummy.SetYTitle(self.plotInfos[-1].yTitle)
        hDummy.SetAxisRange(minEff, maxEff, "Y")
        hDummy.Draw()
        for eff in self.efficiencyGraphs:
            eff.Draw("p same")
        self.canvas.Print(self.plotDir+"/"+self.name+".eps")
        self.canvas.Print(self.plotDir+"/"+self.name+".png")
        self.canvas.Print(self.plotDir+"/"+self.name+".pdf")
        self.canvas.Print(self.plotDir+"/"+self.name+".C")




class EfficiencyPlots:
    def __init__(self):
        self.name = "efficiencies"
        self.divideOption = "cp" ##  Default: Clopper-Pearson interval 
        self.plotDir = "plots"
        self.inputFileNames = []
        self.histoBaseName = "hTagAndProbe_TurnOn"
        self.systems = []
        self.selectionLevels = []
        self.referenceLevels = []
        self.individualNames = []
        self.variables = ["probeele_eta"]
        self.variableNames = {}
        self.minEfficiencies = {}
        self.outputFile = None
        self.plots = []
        self.plotInfos = []

    def addVariable(self, var):
        if not var in self.variables:
            self.variables.append(var)

    def plot(self, minEff=0.95, maxEff=1.01):
        #self.inputFile = ROOT.TFile.Open(self.inputFileName)
        for var in self.variables:
            for plotInfo in self.plotInfos:
                plotInfo.xTitle = self.variableNames[var]
                #plotInfo.yTitle = "efficiency"
            for selectionLevels,referenceLevels,individualName in zip(self.selectionLevels, self.referenceLevels, self.individualNames):
                effPlot = EfficiencyPlot()
                effPlot.name = self.name+"__"+individualName+"__"+var
                effPlot.plotDir = self.plotDir+"/"+self.name+"/"+individualName
                for inputFileName,system,selectionLevel,referenceLevel,plotInfo in zip(self.inputFileNames,self.systems,selectionLevels,referenceLevels,self.plotInfos):
                    inputFile = ROOT.TFile.Open(inputFileName)
                    fvar = "_"+var
                    fselectionLevel = "_"+selectionLevel
                    fsystem = "_"+system if system!="" else ""
                    freferenceLevel = "_"+referenceLevel if referenceLevel!="" else ""
                    passHistoName = self.histoBaseName+fsystem+fselectionLevel+fvar
                    totalHistoName = self.histoBaseName+fsystem+freferenceLevel+fvar
                    passHisto = inputFile.Get(passHistoName)
                    if not passHisto:
                        raise StandardError("Cannot find histo "+passHistoName+" in file "+inputFile.GetName())
                    passHisto.__class__ = ROOT.TH1F
                    passHisto.SetDirectory(0)
                    totalHisto = inputFile.Get(totalHistoName)
                    if not totalHisto:
                        raise StandardError("Cannot find histo "+totalHistoName+" in file "+inputFile.GetName())
                    totalHisto.__class__ = ROOT.TH1F
                    totalHisto.SetDirectory(0)
                    #
                    effPlot.efficiency(passHisto, totalHisto, self.divideOption, plotInfo)
                    effPlot.efficiencyGraphs[-1].SetName(self.name+fsystem+fselectionLevel+freferenceLevel+fvar)
                    inputFile.Close() 
                effPlot.plot(minEff,maxEff)
                self.plots.append(effPlot)
                ## Store efficiencies in output ROOT file
                self.outputFile.cd()
                for graph in effPlot.efficiencyGraphs:
                    graph.Write()
