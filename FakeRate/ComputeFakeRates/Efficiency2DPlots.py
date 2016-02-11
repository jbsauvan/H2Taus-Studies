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
    ROOT.gStyle.SetPadRightMargin(0.13)

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
        self.xTitle = ""
        self.yTitle = ""


class Efficiency2DPlot:
    def __init__(self):
        setPlotStyle()
        self.name = "efficiency"
        self.plotDir = "plots/"
        self.passHisto = None
        self.totalHisto = None
        self.efficiency = None
        self.canvas = None
        self.plotInfo = None

    def addEfficiency(self, pas, total, plotInfo):
        self.passHisto = pas
        self.totalHisto = total
        efficiencyHisto = self.passHisto.Clone("h_"+self.name)
        efficiencyHisto.__class__ = ROOT.TH2F
        efficiencyHisto.Divide(self.totalHisto)
        self.efficiency = efficiencyHisto
        #self.efficiency = ROOT.TGraph2D(efficiencyHisto)
        self.plotInfo = plotInfo

    def plot(self, minEff=0.95, maxEff=1.01):
        setPlotStyle()
        if not os.path.exists(self.plotDir):
            os.makedirs(self.plotDir)
        #np = self.efficiencyGraph.GetN()
        #xMin = self.totalHisto.GetXaxis().GetBinLowEdge(1)
        #xMax = self.totalHisto.GetXaxis().GetBinUpEdge(self.totalHisto.GetNbinsX())
        #yMin = self.totalHisto.GetYaxis().GetBinLowEdge(1)
        #yMax = self.totalHisto.GetYaxis().GetBinUpEdge(self.totalHisto.GetNbinsY())
        self.canvas = ROOT.TCanvas("c_"+self.name, "c_"+self.name, 800, 800)

        #hDummy = ROOT.TH2F("hDummy", "dummy", 1, xMin, xMax, 1, yMin, yMax)
        #hDummy.Draw()
        self.efficiency.SetXTitle(self.plotInfo.xTitle)
        self.efficiency.SetYTitle(self.plotInfo.yTitle)
        self.efficiency.SetAxisRange(minEff, maxEff, "Z")
        self.efficiency.Draw("COLZ")
        #self.efficiencyGraph.Draw("TRI2")
        self.canvas.Print(self.plotDir+"/"+self.name+".eps")
        self.canvas.Print(self.plotDir+"/"+self.name+".png")
        self.canvas.Print(self.plotDir+"/"+self.name+".pdf")
        self.canvas.Print(self.plotDir+"/"+self.name+".C")




class Efficiency2DPlots:
    def __init__(self):
        self.name = "efficiencies"
        self.plotDir = "plots"
        self.inputFileNames = None
        self.histoBaseName = "hTagAndProbe_TurnOn"
        self.selectionLevels = []
        self.referenceLevels = []
        self.individualNames = []
        self.variables = ["probeele_eta"]
        self.variableNames = {}
        self.minEfficiencies = {}
        self.outputFile = None
        self.plots = []
        self.plotInfo = None

    def addVariable(self, var):
        if not var in self.variables:
            self.variables.append(var)

    def plot(self, minEff=0.95, maxEff=1.01):
        for var in self.variables:
            self.plotInfo.xTitle = self.variableNames[var][0]
            self.plotInfo.yTitle = self.variableNames[var][1]
            for selectionLevel,referenceLevel,individualName in zip(self.selectionLevels, self.referenceLevels, self.individualNames):
                effPlot = Efficiency2DPlot()
                effPlot.name = self.name+"__"+individualName+"__"+var
                effPlot.plotDir = self.plotDir+"/"+self.name+"/"+individualName
                fvar = "_"+var
                fselectionLevel = "_"+selectionLevel
                freferenceLevel = "_"+referenceLevel if referenceLevel!="" else ""
                passHistoName = self.histoBaseName+fselectionLevel+fvar
                totalHistoName = self.histoBaseName+freferenceLevel+fvar
                #
                passHistoSum = None
                totalHistoSum = None
                inum = 0
                for inputFileName in self.inputFileNames:
                    inputFile = ROOT.TFile.Open(inputFileName)
                    passHisto = inputFile.Get(passHistoName)
                    if not passHisto:
                        raise StandardError("Cannot find histo "+passHistoName+" in file "+inputFile.GetName())
                    passHisto.__class__ = ROOT.TH2F
                    passHisto.SetDirectory(0)
                    totalHisto = inputFile.Get(totalHistoName)
                    if not totalHisto:
                        raise StandardError("Cannot find histo "+totalHistoName+" in file "+inputFile.GetName())
                    totalHisto.__class__ = ROOT.TH2F
                    totalHisto.SetDirectory(0)
                    #
                    if not passHistoSum: passHistoSum = passHisto.Clone('{0}_{1}_{2}'.format(passHisto.GetName(), self.name, inum))
                    else: passHistoSum.Add(passHisto)
                    if not totalHistoSum: totalHistoSum = totalHisto.Clone('{0}_{1}_{2}'.format(totalHisto.GetName(), self.name, inum))
                    else: totalHistoSum.Add(totalHisto)
                    #
                    inum+= 1
                    inputFile.Close() 
                #
                effPlot.addEfficiency(passHisto, totalHisto, self.plotInfo)
                effPlot.efficiency.SetName(self.name+fselectionLevel+freferenceLevel+fvar)
                effPlot.plot(minEff,maxEff)
                self.plots.append(effPlot)
                ## Store efficiencies in output ROOT file
                self.outputFile.cd()
                effPlot.efficiency.Write()
                inputFile.Close() 

