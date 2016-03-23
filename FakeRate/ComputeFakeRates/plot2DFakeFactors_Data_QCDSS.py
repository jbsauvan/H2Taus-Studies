import ROOT
import os
from Efficiency2DPlots import Efficiency2DPlots, PlotInfo



#inputFileNames = [
    #"../../../Histos/StudyFakeRate/MuTau_FakeRate_QCDSS/Data_Run15D_v4/v_3_2016-02-17/fakerates_MuTau_QCDSS_Data_Run15D_v4.root",
    #"../../../Histos/StudyFakeRate/MuTau_FakeRate_QCDSS/Data_Run15D_05Oct/v_3_2016-02-17/fakerates_MuTau_QCDSS_Data_Run15D_05Oct.root",
#]
inputFileNames = [
    ["../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/Data_Run15D_v4/v_1_2016-03-18/fakerates_MuTau_QCD_Data_Run15D_v4.root",1],
    ["../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/Data_Run15D_05Oct/v_1_2016-03-18/fakerates_MuTau_QCD_Data_Run15D_05Oct.root",1],
]
plotDir = "plots/"
name = "FakeFactors_Data_QCDSS_2D"



selectionLevels = []
selectionLevels.append("SS_IsoRaw_1_5")
selectionLevels.append("SS_Iso_Medium")

selectionLevels2 = []
selectionLevels2.append("SS_IsoRaw_1_5")
selectionLevels2.append("SS_Iso_Medium")
selectionLevels2.append("SS_Iso_Medium")

referenceLevels = []
referenceLevels.append("SS_NoIso")
referenceLevels.append("SS_NoIso")

referenceLevels2 = []
referenceLevels2.append("SS_InvertIsoRaw_1_5")
referenceLevels2.append("SS_InvertIso_Medium")
referenceLevels2.append("SS_InvertIso_Medium_RawOnly")

names = []
names.append("SS_IsoRaw_1_5_Vs_SS_NoIso")
names.append("SS_Iso_Medium_Vs_SS_NoIso")

names2 = []
names2.append("SS_IsoRaw_1_5_Vs_SS_InvertIsoRaw_1_5")
names2.append("SS_Iso_Medium_Vs_SS_InvertIso_Medium")
names2.append("SS_Iso_Medium_Vs_SS_InvertIso_Medium_RawOnly")


variables = ["tau_pt_vs_eta", "tau_pt_vs_decayMode", "tau_pt_vs_pdgId", "tau_pt_vs_mergedPdgId", "tau_jet_pt_vs_decayMode", "tau_jet_pt_vs_pt"]
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
