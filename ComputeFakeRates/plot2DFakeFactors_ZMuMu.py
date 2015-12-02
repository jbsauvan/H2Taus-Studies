import ROOT
import os
from Efficiency2DPlots import Efficiency2DPlots, PlotInfo



inputFileName = "../../Histos/StudyFakeRate/ZMuMu/v_5_2015-12-01/fakerates_ZMuMu.root"
plotDir = "plots/"
name = "2DFakeFactors_ZMuMu"

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

variables = ["tau_pt_vs_eta", "tau_pt_vs_decayMode", "tau_pt_vs_pdgId"]
variableNames = {}
variableNames["tau_pt_vs_eta"] = ["p_{T}^{#tau} [GeV]", "#eta^{#tau}"]
variableNames["tau_pt_vs_decayMode"] = ["p_{T}^{#tau} [GeV]", "decay mode"]
variableNames["tau_pt_vs_pdgId"] = ["p_{T}^{#tau} [GeV]", "pdg ID#times sign-flip"]



plotInfo = PlotInfo()

if not os.path.exists(plotDir+"/"+name):
    os.makedirs(plotDir+"/"+name)
outputFile = ROOT.TFile.Open(plotDir+"/"+name+"/"+name+".root", "RECREATE")

efficiencyPlots = []

effPlots = Efficiency2DPlots()
effPlots.name = name
effPlots.histoBaseName = "hFakeRate"
effPlots.inputFileName = inputFileName
effPlots.selectionLevels = selectionLevels
effPlots.plotInfo = plotInfo
effPlots.referenceLevels = referenceLevels 
effPlots.individualNames = names
effPlots.variables = variables
effPlots.variableNames = variableNames
effPlots.outputFile = outputFile
effPlots.plot(0., 0.2)
efficiencyPlots.append(effPlots)

effPlots = Efficiency2DPlots()
effPlots.name = name
effPlots.histoBaseName = "hFakeRate"
effPlots.inputFileName = inputFileName
effPlots.selectionLevels = selectionLevels
effPlots.plotInfo = plotInfo
effPlots.referenceLevels = referenceLevels2 
effPlots.individualNames = names2
effPlots.variables = variables
effPlots.variableNames = variableNames
effPlots.outputFile = outputFile
effPlots.plot(0., 0.2)
efficiencyPlots.append(effPlots)


outputFile.Close()
