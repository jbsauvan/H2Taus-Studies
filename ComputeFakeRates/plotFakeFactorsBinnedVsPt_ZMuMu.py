import ROOT
import os
from EfficiencyPlots import EfficiencyInBinsPlots, PlotInfo


inputFileName = "../../Histos/StudyFakeRate/ZMuMu/v_6_2015-12-02/fakerates_ZMuMu.root"
plotDir = "plots/"
name = "FakeFactorsInBins_ZMuMu"

systems = []
systems.append("")

selectionLevels = []
selectionLevels.append("StandardIso")

referenceLevels = []
referenceLevels.append("NoIso")

referenceLevels2 = []
referenceLevels2.append("InvertIso")

names = []
names.append("VsNoIso")

names2 = []
names2.append("VsInvertIso")

variables = ["tau_pt_vs_eta_", "tau_pt_vs_decayMode_", "tau_pt_vs_mergedPdgId_"]
variableNames = {}
variableNames["tau_pt_vs_eta_"] = "p_{T}^{#tau} [GeV]"
variableNames["tau_pt_vs_decayMode_"] = "p_{T}^{#tau} [GeV]"
variableNames["tau_pt_vs_pdgId_"] = "p_{T}^{#tau} [GeV]"
variableNames["tau_pt_vs_mergedPdgId_"] = "p_{T}^{#tau} [GeV]"

variableBins = {}
variableBins["tau_pt_vs_eta_"] = [0,1,2]
variableBins["tau_pt_vs_decayMode_"] = [0,1,2]
#variableBins["tau_pt_vs_pdgId_"] = [6,7,8,9,10,11]
variableBins["tau_pt_vs_mergedPdgId_"] = [0,2,3,4,5,6]



colors = [
    ROOT.kMagenta+1,
    ROOT.kBlue+1,
    ROOT.kCyan+1,
    ROOT.kGreen+1,
    ROOT.kYellow,
    ROOT.kOrange+7,
    ROOT.kRed
]

plotInfos = []
for i in xrange(13):
    plotInfos.append(PlotInfo())
    plotInfos[-1].markerStyle = (20 if i<7 else 24)
    plotInfos[-1].markerColor = colors[i%7]
    plotInfos[-1].lineColor = colors[i%7]
    plotInfos[-1].yTitle = "Fake factor" 

if not os.path.exists(plotDir+"/"+name):
    os.makedirs(plotDir+"/"+name)
outputFile = ROOT.TFile.Open(plotDir+"/"+name+"/"+name+".root", "RECREATE")

efficiencyPlots = []

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
effPlots.variableBins = variableBins
effPlots.outputFile = outputFile
effPlots.plot(0., 0.5)
efficiencyPlots.append(effPlots)

effPlots = EfficiencyInBinsPlots()
effPlots.name = name
effPlots.histoBaseName = "hFakeRate"
effPlots.inputFileName = inputFileName
effPlots.selectionLevels = selectionLevels
effPlots.plotInfos = plotInfos
effPlots.referenceLevels = referenceLevels2 
effPlots.individualNames = names2
effPlots.variables = variables
effPlots.variableNames = variableNames
effPlots.variableBins = variableBins
effPlots.outputFile = outputFile
effPlots.divideOption = "pois"
effPlots.plot(0., 0.2)
efficiencyPlots.append(effPlots)


outputFile.Close()
