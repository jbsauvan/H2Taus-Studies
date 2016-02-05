import ROOT
import os
from EfficiencyPlots import EfficiencyInBinsPlots, PlotInfo


inputFileNames = [
    "../../../Histos/StudyFakeRate/MuTau_FakeRateWJetsHighMT/Data_Run15D_v4/v_3_2016-01-29/fakerates_MuTau_WJetsHighMT_Data_Run15D_v4.root",
    "../../../Histos/StudyFakeRate/MuTau_FakeRateWJetsHighMT/Data_Run15D_05Oct/v_3_2016-01-29/fakerates_MuTau_WJetsHighMT_Data_Run15D_05Oct.root",
]
plotDir = "plots/"
name = "FakeFactors_Data_HighMT_Binned"

systems = []
systems.append("")


selectionLevels = []
selectionLevels.append("IsoRaw_1_5")
selectionLevels.append("Iso_Medium")

selectionLevels2 = []
selectionLevels2.append("IsoRaw_1_5")
selectionLevels2.append("Iso_Medium")
selectionLevels2.append("Iso_Medium")

referenceLevels = []
referenceLevels.append("NoIso")
referenceLevels.append("NoIso")

referenceLevels2 = []
referenceLevels2.append("InvertIsoRaw_1_5")
referenceLevels2.append("InvertIso_Medium")
referenceLevels2.append("InvertIso_Medium_RawOnly")

names = []
names.append("IsoRaw_1_5_Vs_NoIso")
names.append("Iso_Medium_VsNoIso")

names2 = []
names2.append("IsoRaw_1_5_Vs_InvertIsoRaw_1_5")
names2.append("Iso_Medium_Vs_InvertIso_Medium")
names2.append("Iso_Medium_Vs_InvertIso_Medium_RawOnly")

variables = ["tau_pt_vs_eta_", "tau_pt_vs_decayMode_", "tau_pt_vs_mergedPdgId_", "tau_jet_pt_vs_pt_", "tau_jet_pt_vs_decayMode_"]
variableNames = {}
variableNames["tau_pt_vs_eta_"] = "p_{T}^{#tau} [GeV]"
variableNames["tau_pt_vs_decayMode_"] = "p_{T}^{#tau} [GeV]"
variableNames["tau_pt_vs_pdgId_"] = "p_{T}^{#tau} [GeV]"
variableNames["tau_pt_vs_mergedPdgId_"] = "p_{T}^{#tau} [GeV]"
variableNames["tau_jet_pt_vs_pt_"] = "p_{T}^{jet} [GeV]"
variableNames["tau_jet_pt_vs_decayMode_"] = "p_{T}^{jet} [GeV]"

variableBins = {}
variableBins["tau_pt_vs_eta_"] = [0,1,2]
variableBins["tau_pt_vs_decayMode_"] = [0,1,2]
#variableBins["tau_pt_vs_pdgId_"] = [6,7,8,9,10,11]
variableBins["tau_pt_vs_mergedPdgId_"] = [0,2,3,4,5,6]
variableBins["tau_jet_pt_vs_pt_"] = [0,1,2]
variableBins["tau_jet_pt_vs_decayMode_"] = [0,1,2]

variableLegends = {}
variableLegends["tau_pt_vs_eta_"] = ["0<|#eta|<0.8","0.8<|#eta|<1.5","1.5<|#eta|<2.5"]
variableLegends["tau_pt_vs_decayMode_"] = ["decay=0","decay=1","decay=10"]
variableLegends["tau_pt_vs_mergedPdgId_"] = ["sign-flip","d","u+s","c","b","gluon"]
variableLegends["tau_jet_pt_vs_pt_"] = ["20<p_{T}^{#tau}<30","30<p_{T}^{#tau}<60","60<p_{T}^{#tau}<200"]
variableLegends["tau_jet_pt_vs_decayMode_"] = ["decay=0","decay=1","decay=10"]



colors = [
    ROOT.kMagenta+1,
    ROOT.kBlue+1,
    ROOT.kCyan+1,
    ROOT.kGreen+1,
    ROOT.kOrange+7,
    ROOT.kRed,
    ROOT.kMagenta,
]

markers = [
    20,
    24,
    20,
    24,
    20,
    24,
    20
]

plotInfos = []
for i in xrange(13):
    plotInfos.append(PlotInfo())
    plotInfos[-1].markerStyle = markers[i%7]
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
effPlots.inputFileNames = inputFileNames
effPlots.selectionLevels = selectionLevels
effPlots.plotInfos = plotInfos
effPlots.referenceLevels = referenceLevels 
effPlots.individualNames = names
effPlots.variables = variables
effPlots.variableNames = variableNames
effPlots.variableLegends = variableLegends
effPlots.variableBins = variableBins
effPlots.outputFile = outputFile
effPlots.plot(0., 0.5)
efficiencyPlots.append(effPlots)

effPlots = EfficiencyInBinsPlots()
effPlots.name = name
effPlots.histoBaseName = "hFakeRate"
effPlots.inputFileNames = inputFileNames
effPlots.selectionLevels = selectionLevels2
effPlots.plotInfos = plotInfos
effPlots.referenceLevels = referenceLevels2 
effPlots.individualNames = names2
effPlots.variables = variables
effPlots.variableNames = variableNames
effPlots.variableLegends = variableLegends
effPlots.variableBins = variableBins
effPlots.outputFile = outputFile
effPlots.divideOption = "pois"
effPlots.plot(0., 0.5)
efficiencyPlots.append(effPlots)


outputFile.Close()
