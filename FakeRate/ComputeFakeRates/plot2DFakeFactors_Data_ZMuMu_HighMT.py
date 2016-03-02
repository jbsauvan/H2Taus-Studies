import ROOT
import os
from Efficiency2DPlots import Efficiency2DPlots, PlotInfo



inputFileNames = [
    "../../../Histos/StudyFakeRate/MuMu_MTStudy/76X/Data_Run15D/v_1_2016-03-01/fakerates_ZMuMu_MTStudy_Data_Run15D.root",
]
plotDir = "plots/"
name = "FakeFactors_Data_ZMuMu_HighMT_2D"


selectionLevels2 = []
selectionLevels2.append("MTgt70_Iso_Medium")


referenceLevels2 = []
referenceLevels2.append("MTgt70_InvertIso_Medium")


names2 = []
names2.append("Iso_Medium_Vs_InvertIso_Medium")


variables = ["tau_pt_vs_decayMode"]
variableNames = {}
variableNames["tau_pt_vs_eta"] = ["p_{T}^{#tau} [GeV]", "#eta^{#tau}"]
variableNames["tau_pt_vs_decayMode"] = ["p_{T}^{#tau} [GeV]", "decay mode"]
variableNames["tau_pt_vs_pdgId"] = ["p_{T}^{#tau} [GeV]", "pdg ID#times sign-flip"]
variableNames["tau_pt_vs_mergedPdgId"] = ["p_{T}^{#tau} [GeV]", "pdg ID#times sign-flip"]
variableNames["tau_jet_pt_vs_decayMode"] = ["p_{T}^{jet} [GeV]", "decay mode"]
variableNames["tau_jet_pt_vs_pt"] = ["p_{T}^{jet} [GeV]", "p_{T}^{#tau} [GeV]"]



plotInfo = PlotInfo()

if not os.path.exists(plotDir+"/"+name):
    os.makedirs(plotDir+"/"+name)
outputFile = ROOT.TFile.Open(plotDir+"/"+name+"/"+name+".root", "RECREATE")

efficiencyPlots = []


effPlots = Efficiency2DPlots()
effPlots.name = name
effPlots.histoBaseName = "hFakeRate"
effPlots.inputFileNames = inputFileNames
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
