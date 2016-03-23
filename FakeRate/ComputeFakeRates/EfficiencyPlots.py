import ROOT
import os
import array


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
        self.legend = ""
        self.xTitle = ""
        self.yTitle = ""



class EfficiencyPlot:
    def __init__(self):
        self.name = "efficiency"
        self.plotDir = "plots/"
        self.publicationDir = ""
        self.passHistos = []
        self.totalHistos = []
        self.efficiencyGraphs = []
        self.efficiencyHistos = []
        self.canvas = None
        self.drawLegend = False
        self.legendPosition = [0.6, 0.7, 0.95, 0.9]
        self.plotInfos = []

    def efficiency(self, pas, total, option, plotInfo):
        self.passHistos.append(pas)
        self.totalHistos.append(total)
        self.efficiencyGraphs.append(ROOT.TGraphAsymmErrors())
        self.efficiencyGraphs[-1].Divide(pas,total, option)
        self.efficiencyGraphs[-1].SetMarkerStyle(plotInfo.markerStyle)
        self.efficiencyGraphs[-1].SetMarkerColor(plotInfo.markerColor)
        self.efficiencyGraphs[-1].SetLineColor(plotInfo.lineColor)
        self.efficiencyHistos.append(pas.Clone())
        self.efficiencyHistos[-1].__class__ = ROOT.TH1F
        self.efficiencyHistos[-1].SetDirectory(0)
        p = 0
        for b in xrange(1,pas.GetNbinsX()+1):
            if total.GetBinContent(b)==0:
                self.efficiencyHistos[-1].SetBinContent(b, 0)
                self.efficiencyHistos[-1].SetBinError(b, 0)
                continue
            eff = self.efficiencyGraphs[-1].GetY()[p]
            eup = self.efficiencyGraphs[-1].GetEYhigh()[p]
            edown = self.efficiencyGraphs[-1].GetEYlow()[p]
            error = (eup+edown)/2.
            self.efficiencyHistos[-1].SetBinContent(b, eff)
            self.efficiencyHistos[-1].SetBinError(b, error)
            p += 1
        ## Fill under/over-flows
        self.efficiencyHistos[-1].SetBinContent(0, self.efficiencyHistos[-1].GetBinContent(1))
        self.efficiencyHistos[-1].SetBinContent(pas.GetNbinsX()+1, self.efficiencyHistos[-1].GetBinContent(pas.GetNbinsX()))
        self.plotInfos.append(plotInfo)

    def addGraph(self, graph, plotInfo):
        self.efficiencyGraphs.append(graph)
        self.efficiencyGraphs[-1].SetMarkerStyle(plotInfo.markerStyle)
        self.efficiencyGraphs[-1].SetMarkerColor(plotInfo.markerColor)
        self.efficiencyGraphs[-1].SetLineColor(plotInfo.lineColor)
        self.plotInfos.append(plotInfo)

    def plot(self, minEff=0.95, maxEff=1.01):
        setPlotStyle()
        if not os.path.exists(self.plotDir):
            os.makedirs(self.plotDir)
        if self.publicationDir!="" and not os.path.exists(self.publicationDir):
            os.makedirs(self.publicationDir)
        np = self.efficiencyGraphs[-1].GetN()
        if len(self.totalHistos)>0 and self.totalHistos[-1]:
            xMin = self.totalHistos[-1].GetXaxis().GetBinLowEdge(1)
            xMax = self.totalHistos[-1].GetXaxis().GetBinUpEdge(self.totalHistos[-1].GetNbinsX())
        else:
            xMin = self.efficiencyGraphs[-1].GetX()[0]-self.efficiencyGraphs[-1].GetEXlow()[0]
            xMax = self.efficiencyGraphs[-1].GetX()[np-1]+self.efficiencyGraphs[-1].GetEXlow()[np-1]
        self.canvas = ROOT.TCanvas("c_"+self.name, "c_"+self.name, 800, 800)
        self.canvas.SetGrid()

        hDummy = ROOT.TH1F("hDummy", "dummy", 1, xMin, xMax)
        hDummy.SetXTitle(self.plotInfos[-1].xTitle)
        hDummy.SetYTitle(self.plotInfos[-1].yTitle)
        hDummy.SetAxisRange(minEff, maxEff, "Y")
        hDummy.Draw()
        legend = ROOT.TLegend(self.legendPosition[0],self.legendPosition[1],self.legendPosition[2],self.legendPosition[3])
        legend.SetFillColor(0)
        legend.SetLineColor(0)
        for eff,plotInfo in zip(self.efficiencyGraphs, self.plotInfos):
            eff.Draw("p same")
            legend.AddEntry(eff, plotInfo.legend, "p")
        if self.drawLegend: legend.Draw()
        self.canvas.Print(self.plotDir+"/"+self.name+".eps")
        self.canvas.Print(self.plotDir+"/"+self.name+".png")
        self.canvas.Print(self.plotDir+"/"+self.name+".pdf")
        #self.canvas.Print(self.plotDir+"/"+self.name+".C")
        if self.publicationDir!="":
            self.canvas.Print(self.publicationDir+"/"+self.name+".eps")
            self.canvas.Print(self.publicationDir+"/"+self.name+".png")
            self.canvas.Print(self.publicationDir+"/"+self.name+".pdf")
            #self.canvas.Print(self.publicationDir+"/"+self.name+".C")


class DataMCEfficiencyPlot:
    def __init__(self):
        self.name = 'efficiencies'
        self.divideOption = "cp" ##  Default: Clopper-Pearson interval
        self.rebin = 1
        self.plotDir = "plots"
        self.selectionHistoName = ''
        self.referenceHistoName = ''
        self.dataFileNames = []
        self.mcFileNames = []
        self.mcRescalings = []
        self.referenceMC = False
        self.dataPlotInfo = None
        self.mcPlotInfo = None
        self.referencePlotInfo = None
        self.outputFile = None
        self.plots = []


    def plot(self, minEff=0.95, maxEff=1.01):
        effPlot = EfficiencyPlot()
        effPlot.name = self.name
        effPlot.plotDir = self.plotDir
        dataPassHisto = None
        dataTotalHisto = None
        mcPassHisto = None
        mcTotalHisto = None
        refPassHisto = None
        refTotalHisto = None
        idata = 0
        #### Data
        for dataFileName in self.dataFileNames:
            inputFile = ROOT.TFile.Open(dataFileName)
            passHisto = inputFile.Get(self.selectionHistoName)
            if not passHisto:
                raise StandardError("Cannot find histo "+self.selectionHistoName)
            passHisto.__class__ = ROOT.TH1F
            passHisto.SetDirectory(0)
            if self.rebin>1: passHisto.Rebin(self.rebin)
            totalHisto = inputFile.Get(self.referenceHistoName)
            if not totalHisto:
                raise StandardError("Cannot find histo "+self.referenceHistoName)
            totalHisto.__class__ = ROOT.TH1F
            totalHisto.SetDirectory(0)
            if self.rebin>1: totalHisto.Rebin(self.rebin)
            #
            inputFile.Close()
            if not dataPassHisto: dataPassHisto = passHisto.Clone('{0}_{1}_Data_{2}'.format(passHisto.GetName(), self.name, idata))
            else: dataPassHisto.Add(passHisto)
            if not dataTotalHisto: dataTotalHisto = totalHisto.Clone('{0}_{1}_Data_{2}'.format(totalHisto.GetName(), self.name, idata))
            else: dataTotalHisto.Add(totalHisto)
            #
            idata += 1
        #### MC
        imc = 0
        for mcFileName,mcRescaling in zip(self.mcFileNames, self.mcRescalings):
            inputFile = ROOT.TFile.Open(mcFileName)
            passHisto = inputFile.Get(self.selectionHistoName)
            if not passHisto:
                raise StandardError("Cannot find histo "+self.selectionHistoName)
            passHisto.__class__ = ROOT.TH1F
            passHisto.SetDirectory(0)
            passHisto.Scale(mcRescaling)
            if self.rebin>1: passHisto.Rebin(self.rebin)
            totalHisto = inputFile.Get(self.referenceHistoName)
            if not totalHisto:
                raise StandardError("Cannot find histo "+self.referenceHistoName)
            totalHisto.__class__ = ROOT.TH1F
            totalHisto.SetDirectory(0)
            totalHisto.Scale(mcRescaling)
            if self.rebin>1: totalHisto.Rebin(self.rebin)
            #
            inputFile.Close()
            if not mcPassHisto: mcPassHisto = passHisto.Clone('{0}_{1}_MC_{2}'.format(passHisto.GetName(), self.name, imc))
            else: mcPassHisto.Add(passHisto)
            if not mcTotalHisto: mcTotalHisto = totalHisto.Clone('{0}_{1}_MC_{2}'.format(totalHisto.GetName(), self.name, imc))
            else: mcTotalHisto.Add(totalHisto)
            #
            if imc==0 and self.referenceMC:
                refPassHisto = passHisto.Clone('{0}_{1}_Ref'.format(passHisto.GetName(), self.name))
                refTotalHisto = totalHisto.Clone('{0}_{1}_Ref'.format(totalHisto.GetName(), self.name))
            imc += 1
        #
        effPlot.efficiency(dataPassHisto, dataTotalHisto, self.divideOption, self.dataPlotInfo)
        effPlot.efficiencyGraphs[-1].SetName('{0}_Data'.format(self.name))
        #
        effPlot.efficiency(mcPassHisto, mcTotalHisto, self.divideOption, self.mcPlotInfo)
        effPlot.efficiencyGraphs[-1].SetName('{0}_MC'.format(self.name))
        #
        if refPassHisto and refTotalHisto:
            effPlot.efficiency(refPassHisto, refTotalHisto, self.divideOption, self.referencePlotInfo)
            effPlot.efficiencyGraphs[-1].SetName('{0}_Ref'.format(self.name))
        effPlot.drawLegend = True
        effPlot.plot(minEff,maxEff)
        self.plots.append(effPlot)
        ## Store efficiencies in output ROOT file
        self.outputFile.cd()
        for graph in effPlot.efficiencyGraphs:
            graph.Write()




class EfficiencyPlots:
    def __init__(self):
        self.name = "efficiencies"
        self.divideOption = "cp" ##  Default: Clopper-Pearson interval
        self.rebin = 1
        self.plotDir = "plots"
        self.publicationDir = ""
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
                if self.publicationDir!="": effPlot.publicationDir = self.publicationDir+"/"+self.name+"/"+individualName
                for inputFileNames,system,selectionLevel,referenceLevel,plotInfo in zip(self.inputFileNames,self.systems,selectionLevels,referenceLevels,self.plotInfos):
                    fvar = "_"+var
                    fselectionLevel = "_"+selectionLevel
                    fsystem = "_"+system if system!="" else ""
                    freferenceLevel = "_"+referenceLevel if referenceLevel!="" else ""
                    passHistoName = self.histoBaseName+fsystem+fselectionLevel+fvar
                    totalHistoName = self.histoBaseName+fsystem+freferenceLevel+fvar
                    #
                    passHistoSum = None
                    totalHistoSum = None
                    inum = 0
                    for inputFileName,weight in inputFileNames:
                        inputFile = ROOT.TFile.Open(inputFileName)
                        passHisto = inputFile.Get(passHistoName)
                        if not passHisto:
                            raise StandardError("Cannot find histo "+passHistoName+" in file "+inputFile.GetName())
                        passHisto.__class__ = ROOT.TH1F
                        passHisto.SetDirectory(0)
                        if self.rebin.__class__==list: 
                            passHisto = passHisto.Rebin(len(self.rebin)-1, passHisto.GetName()+'_rebin', array.array('d',self.rebin))
                            passHisto.__class__ = ROOT.TH1F
                            passHisto.SetDirectory(0)
                        elif self.rebin>1: passHisto.Rebin(self.rebin)
                        totalHisto = inputFile.Get(totalHistoName)
                        if not totalHisto:
                            raise StandardError("Cannot find histo "+totalHistoName+" in file "+inputFile.GetName())
                        totalHisto.__class__ = ROOT.TH1F
                        totalHisto.SetDirectory(0)
                        if self.rebin.__class__==list: 
                            totalHisto = totalHisto.Rebin(len(self.rebin)-1, totalHisto.GetName()+'_rebin', array.array('d',self.rebin))
                            totalHisto.__class__ = ROOT.TH1F
                            totalHisto.SetDirectory(0)
                        elif self.rebin>1: totalHisto.Rebin(self.rebin)
                        #
                        inputFile.Close()
                        if not passHistoSum: 
                            passHistoSum = passHisto.Clone('{0}_{1}_{2}'.format(passHisto.GetName(), self.name, inum))
                            passHistoSum.Scale(weight)
                        else: passHistoSum.Add(passHisto, weight)
                        if not totalHistoSum: 
                            totalHistoSum = totalHisto.Clone('{0}_{1}_{2}'.format(totalHisto.GetName(), self.name, inum))
                            totalHistoSum.Scale(weight)
                        else: totalHistoSum.Add(totalHisto, weight)
                        #
                        inum+= 1
                    #
                    effPlot.efficiency(passHistoSum, totalHistoSum, self.divideOption, plotInfo)
                    effPlot.efficiencyGraphs[-1].SetName(self.name+fsystem+fselectionLevel+freferenceLevel+fvar)
                    inputFile.Close()
                effPlot.plot(minEff,maxEff)
                self.plots.append(effPlot)
                ## Store efficiencies in output ROOT file
                self.outputFile.cd()
                for graph in effPlot.efficiencyGraphs:
                    graph.Write()


class EfficiencyInBinsPlots:
    def __init__(self):
        self.name = "efficiencies"
        self.divideOption = "cp" ##  Default: Clopper-Pearson interval
        self.plotDir = "plots"
        self.inputFileNames = None
        self.histoBaseName = "hTagAndProbe_TurnOn"
        self.selectionLevels = []
        self.referenceLevels = []
        self.individualNames = []
        self.variables = ["probeele_eta"]
        self.variableNames = {}
        self.variableLegends = {}
        self.variableBins = {}
        self.minEfficiencies = {}
        self.outputFile = None
        self.plots = []
        self.plotInfos = []

    def addVariable(self, var):
        if not var in self.variables:
            self.variables.append(var)

    def plot(self, minEff=0.95, maxEff=1.01):
        for var in self.variables:
            for plotInfo in self.plotInfos:
                plotInfo.xTitle = self.variableNames[var]
                #plotInfo.yTitle = "efficiency"
            for selectionLevel,referenceLevel,individualName in zip(self.selectionLevels, self.referenceLevels, self.individualNames):
                effPlot = EfficiencyPlot()
                effPlot.drawLegend = True
                effPlot.name = self.name+"__"+individualName+"__"+var
                effPlot.plotDir = self.plotDir+"/"+self.name+"/"+individualName
                for bin,plotInfo,legend in zip(self.variableBins[var],self.plotInfos,self.variableLegends[var]):
                    plotInfo.legend = legend
                    fvar = "_"+var
                    fselectionLevel = "_"+selectionLevel
                    fbin = str(bin)
                    freferenceLevel = "_"+referenceLevel if referenceLevel!="" else ""
                    passHistoName = self.histoBaseName+fselectionLevel+fvar+fbin
                    totalHistoName = self.histoBaseName+freferenceLevel+fvar+fbin
                    #
                    passHistoSum = None
                    totalHistoSum = None
                    inum = 0
                    for inputFileName,weight in self.inputFileNames:
                        inputFile = ROOT.TFile.Open(inputFileName)
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
                        inputFile.Close()
                        if not passHistoSum: 
                            passHistoSum = passHisto.Clone('{0}_{1}_{2}'.format(passHisto.GetName(), self.name, inum))
                            passHistoSum.Scale(weight)
                        else: passHistoSum.Add(passHisto, weight)
                        if not totalHistoSum: 
                            totalHistoSum = totalHisto.Clone('{0}_{1}_{2}'.format(totalHisto.GetName(), self.name, inum))
                            totalHistoSum.Scale(weight)
                        else: totalHistoSum.Add(totalHisto, weight)
                        #
                        inum+= 1
                    #
                    effPlot.efficiency(passHistoSum, totalHistoSum, self.divideOption, plotInfo)
                    effPlot.efficiencyGraphs[-1].SetName(self.name+fselectionLevel+freferenceLevel+fvar+fbin)
                effPlot.plot(minEff,maxEff)
                self.plots.append(effPlot)
                ## Store efficiencies in output ROOT file
                self.outputFile.cd()
                for graph in effPlot.efficiencyGraphs:
                    graph.Write()
