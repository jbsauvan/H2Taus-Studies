import ROOT
import os
from EfficiencyPlots import EfficiencyInBinsPlots, PlotInfo

publish = False
publicationDir = ""
#if publish:
    #if os.path.exists("/afs/cern.ch/user/j/jsauvan/www/"):
        #publicationDir = "/afs/cern.ch/user/j/jsauvan/www/H2Taus/FakeRate/FakeFactors/"
    #elif os.path.exists("/home/sauvan/lxplus/www/"):
        #publicationDir = "/home/sauvan/lxplus/www/H2Taus/FakeRate/FakeFactors/"
    #else:
        #publish = False


inputFileName = "../../../Histos/StudyFakeRate/MuTau_WJets/W/v_1_2016-01-07/fakerates_MuTau_WJets_W.root"
plotDir = "plots/"
name = "FakeFactors_WJets"
systems = []
systems.append("")


selectionLevels = []
selectionLevels.append("Iso_Medium_OS")
selectionLevels.append("Iso_Medium_SS")


referenceLevels = []
referenceLevels.append("InvertIso_Medium_OS")
referenceLevels.append("InvertIso_Medium_SS")

names = []
names.append("Iso_Medium_OS_Vs_InvertIso_Medium_OS")
names.append("Iso_Medium_SS_Vs_InvertIso_Medium_SS")

variables = ["tau_pt_vs_mt_", "tau_pdgId_vs_mt_"]
variableNames = {}
for var in variables:
    if 'tau_pt' in var: variableNames[var] = "p_{T}^{#tau} [GeV]"
    if 'tau_pdgId' in var: variableNames[var] = "|pdg ID| #times sign-flip"

variableBins = {}
variableBins["tau_pt_vs_mt_"] = [0,1,2]
variableBins["tau_pdgId_vs_mt_"] = [0,1,2]

variableLegends = {}
variableLegends["tau_pt_vs_mt_"] = ["M_{T} < 40GeV","40 < M_{T} < 80GeV","M_{T} > 80GeV"]
variableLegends["tau_pdgId_vs_mt_"] = ["M_{T} < 40GeV","40 < M_{T} < 80GeV","M_{T} > 80GeV"]



colors = [
    ROOT.kBlack,
    ROOT.kRed,
    ROOT.kRed,
]

markers = [
    20,
    20,
    24,
]


plotInfos = []
for i in xrange(3):
    plotInfos.append(PlotInfo())
    plotInfos[-1].markerStyle = markers[i]
    plotInfos[-1].markerColor = colors[i]
    plotInfos[-1].lineColor = colors[i]
    plotInfos[-1].yTitle = "Fake factor"


if not os.path.exists(plotDir+"/"+name):
    os.makedirs(plotDir+"/"+name)
outputFile = ROOT.TFile.Open(plotDir+"/"+name+"/"+name+".root", "RECREATE")

efficiencyPlots = []


#effPlots = EfficiencyPlots()
#effPlots.name = name
#effPlots.publicationDir = publicationDir
#effPlots.histoBaseName = "hFakeRate"
#effPlots.inputFileNames = [inputFileName]
#effPlots.systems = systems
#effPlots.selectionLevels = selectionLevels
#effPlots.plotInfos = plotInfos
#effPlots.referenceLevels = referenceLevels 
#effPlots.individualNames = names
#effPlots.variables = variables
#effPlots.variableNames = variableNames
#effPlots.outputFile = outputFile
#effPlots.divideOption = "pois"
#effPlots.plot(0., 0.5)
#efficiencyPlots.append(effPlots)

effPlots = EfficiencyInBinsPlots()
effPlots.name = name
effPlots.histoBaseName = "hFakeRate"
effPlots.inputFileName = inputFileName
effPlots.selectionLevels = selectionLevels
effPlots.plotInfos = plotInfos
effPlots.referenceLevels = referenceLevels 
effPlots.individualNames = names
effPlots.variables = variables
effPlots.variableNames = variableNames
effPlots.variableLegends = variableLegends
effPlots.variableBins = variableBins
effPlots.outputFile = outputFile
effPlots.divideOption = "pois"
effPlots.plot(0., 0.3)
efficiencyPlots.append(effPlots)


outputFile.Close()
