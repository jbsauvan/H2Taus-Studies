import ROOT
import os
from EfficiencyPlots import EfficiencyPlots, PlotInfo



inputFileName = "../../Histos/StudyFakeRate/ZMuMu/v_4_2015-11-25/fakerates_ZMuMu.root"
plotDir = "plots/"
name = "FakeFactors_ZMuMu"
systems = []
systems.append("")

selectionLevels = []
selectionLevels.append(("StandardIso",))

referenceLevels = []
referenceLevels.append(("NoIso",))

referenceLevels2 = []
referenceLevels2.append(("InvertIso",))

names = []
names.append("VsNoIso")

names2 = []
names2.append("VsInvertIso")

variables = ["tau_pt", "tau_eta", "tau_decayMode", "tau_pdgId", "nevents", "nvertices", "rho"]
variableNames = {}
variableNames["tau_pt"] = "p_{T}^{#tau} [GeV]"
variableNames["tau_eta"] = "#eta^{#tau}"
variableNames["tau_decayMode"] = "decayMode"
variableNames["tau_pdgId"] = "pdg ID"
variableNames["nevents"] = ""
variableNames["nvertices"] = "N_{PV}"
variableNames["rho"] = "#rho"



plotInfos = [PlotInfo()]
plotInfos[0].markerStyle = 20
plotInfos[0].yTitle = "Fake factor" 

if not os.path.exists(plotDir+"/"+name):
    os.makedirs(plotDir+"/"+name)
outputFile = ROOT.TFile.Open(plotDir+"/"+name+"/"+name+".root", "RECREATE")

efficiencyPlots = []

effPlots = EfficiencyPlots()
effPlots.name = name
effPlots.histoBaseName = "hFakeRate"
effPlots.inputFileNames = [inputFileName]
effPlots.systems = systems
effPlots.selectionLevels = selectionLevels
effPlots.plotInfos = plotInfos
effPlots.referenceLevels = referenceLevels 
effPlots.individualNames = names
effPlots.variables = variables
effPlots.variableNames = variableNames
effPlots.outputFile = outputFile
effPlots.plot(0., 0.5)
efficiencyPlots.append(effPlots)

effPlots = EfficiencyPlots()
effPlots.name = name
effPlots.histoBaseName = "hFakeRate"
effPlots.inputFileNames = [inputFileName]
effPlots.systems = systems
effPlots.selectionLevels = selectionLevels
effPlots.plotInfos = plotInfos
effPlots.referenceLevels = referenceLevels2 
effPlots.individualNames = names2
effPlots.variables = variables
effPlots.variableNames = variableNames
effPlots.outputFile = outputFile
effPlots.divideOption = "pois"
effPlots.plot(0., 0.5)
efficiencyPlots.append(effPlots)


outputFile.Close()
