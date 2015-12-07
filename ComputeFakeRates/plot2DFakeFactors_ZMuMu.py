import ROOT
import os
from Efficiency2DPlots import Efficiency2DPlots, PlotInfo



inputFileName = "../../Histos/StudyFakeRate/ZMuMu/v_7_2015-12-05/fakerates_ZMuMu.root"
plotDir = "plots/"
name = "FakeFactors_ZMuMu_2D"



selectionLevels = []
selectionLevels.append("IsoRaw_1_5")
selectionLevels.append("Iso_Medium")

selectionLevels2 = []
selectionLevels2.append("IsoRaw_1_5")
selectionLevels2.append("IsoRaw_1_5")
selectionLevels2.append("Iso_Medium")

referenceLevels = []
referenceLevels.append("NoIso")
referenceLevels.append("NoIso")

referenceLevels2 = []
referenceLevels2.append("InvertIsoRaw_1_5")
referenceLevels2.append("InvertIsoRaw_3")
referenceLevels2.append("InvertIso_Medium")

names = []
names.append("IsoRaw_1_5_Vs_NoIso")
names.append("Iso_Medium_VsNoIso")

names2 = []
names2.append("IsoRaw_1_5_Vs_InvertIsoRaw_1_5")
names2.append("IsoRaw_1_5_Vs_InvertIsoRaw_3")
names2.append("Iso_Medium_Vs_InvertIso_Medium")


variables = ["tau_pt_vs_eta", "tau_pt_vs_decayMode", "tau_pt_vs_pdgId", "tau_pt_vs_mergedPdgId"]
variableNames = {}
variableNames["tau_pt_vs_eta"] = ["p_{T}^{#tau} [GeV]", "#eta^{#tau}"]
variableNames["tau_pt_vs_decayMode"] = ["p_{T}^{#tau} [GeV]", "decay mode"]
variableNames["tau_pt_vs_pdgId"] = ["p_{T}^{#tau} [GeV]", "pdg ID#times sign-flip"]
variableNames["tau_pt_vs_mergedPdgId"] = ["p_{T}^{#tau} [GeV]", "pdg ID#times sign-flip"]



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
effPlots.selectionLevels = selectionLevels2
effPlots.plotInfo = plotInfo
effPlots.referenceLevels = referenceLevels2 
effPlots.individualNames = names2
effPlots.variables = variables
effPlots.variableNames = variableNames
effPlots.outputFile = outputFile
effPlots.plot(0., 0.2)
efficiencyPlots.append(effPlots)


outputFile.Close()
