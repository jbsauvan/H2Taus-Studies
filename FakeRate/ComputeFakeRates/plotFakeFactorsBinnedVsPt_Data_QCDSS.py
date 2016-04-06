import ROOT
import os
import pickle
from EfficiencyPlots import EfficiencyInBinsPlots, PlotInfo

mc_info = pickle.load(open('mc_info.pck', 'rb'))
int_lumi = 2094.2

#inputFileNames = [
    #"../../../Histos/StudyFakeRate/MuTau_FakeRate_QCDSS/Data_Run15D_v4/v_3_2016-02-17/fakerates_MuTau_QCDSS_Data_Run15D_v4.root",
    #"../../../Histos/StudyFakeRate/MuTau_FakeRate_QCDSS/Data_Run15D_05Oct/v_3_2016-02-17/fakerates_MuTau_QCDSS_Data_Run15D_05Oct.root",
#]

inputFileNames = [
    # Data
    ["../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/Data_Run15D_v4/v_2_2016-04-05/fakerates_MuTau_QCD_Data_Run15D_v4.root", 1.],
    ["../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/Data_Run15D_05Oct/v_2_2016-04-05/fakerates_MuTau_QCD_Data_Run15D_05Oct.root", 1.],
    # Subtract MC
    ['../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/W/v_2_2016-04-05/fakerates_MuTau_QCD_W.root', 
     -int_lumi*mc_info['W']['XSec']          /mc_info['W']['SumWeights'],],
    ['../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/Z/v_2_2016-04-05/fakerates_MuTau_QCD_Z.root',
     -int_lumi*mc_info['ZJ']['XSec']         /mc_info['ZJ']['SumWeights'],],
    ['../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/TT/v_2_2016-04-05/fakerates_MuTau_QCD_TT.root',
     -int_lumi*mc_info['TT']['XSec']         /mc_info['TT']['SumWeights'],],
    ['../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/T_tWch/v_2_2016-04-05/fakerates_MuTau_QCD_T_tWch.root',
     -int_lumi*mc_info['T_tWch']['XSec']     /mc_info['T_tWch']['SumWeights'],],
    ['../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/TBar_tWch/v_2_2016-04-05/fakerates_MuTau_QCD_TBar_tWch.root',
     -int_lumi*mc_info['TBar_tWch']['XSec']  /mc_info['TBar_tWch']['SumWeights'],],
    ['../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/VVTo2L2Nu/v_2_2016-04-05/fakerates_MuTau_QCD_VVTo2L2Nu.root',
     -int_lumi*mc_info['VVTo2L2Nu']['XSec']  /mc_info['VVTo2L2Nu']['SumWeights'],],
    ['../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/WZTo2L2Q/v_2_2016-04-05/fakerates_MuTau_QCD_WZTo2L2Q.root',
     -int_lumi*mc_info['WZTo2L2Q']['XSec']   /mc_info['WZTo2L2Q']['SumWeights'],],
    ['../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/WZTo1L3Nu/v_2_2016-04-05/fakerates_MuTau_QCD_WZTo1L3Nu.root',
     -int_lumi*mc_info['WZTo1L3Nu']['XSec']  /mc_info['WZTo1L3Nu']['SumWeights'],],
    ['../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/WZTo3L/v_2_2016-04-05/fakerates_MuTau_QCD_WZTo3L.root',
     -int_lumi*mc_info['WZTo3L']['XSec']     /mc_info['WZTo3L']['SumWeights'],],
    ['../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/WZTo1L1Nu2Q/v_2_2016-04-05/fakerates_MuTau_QCD_WZTo1L1Nu2Q.root',
     -int_lumi*mc_info['WZTo1L1Nu2Q']['XSec']/mc_info['WZTo1L1Nu2Q']['SumWeights'],],
    ['../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/ZZTo2L2Q/v_2_2016-04-05/fakerates_MuTau_QCD_ZZTo2L2Q.root',
     -int_lumi*mc_info['ZZTo2L2Q']['XSec']   /mc_info['ZZTo2L2Q']['SumWeights'],],
    ['../../../Histos/StudyFakeRate/MuTau_FakeRate_QCD/WWTo1L1Nu2Q/v_2_2016-04-05/fakerates_MuTau_QCD_WWTo1L1Nu2Q.root',
     -int_lumi*mc_info['WWTo1L1Nu2Q']['XSec']/mc_info['WWTo1L1Nu2Q']['SumWeights'],],
]

plotDir = "plots/"
name = "FakeFactors_Data_QCDSS_Binned"

systems = []
systems.append("")


selectionLevels = []
selectionLevels.append("SS_IsoRaw_1_5")
selectionLevels.append("SS_Iso_Medium")

selectionLevels2 = []
selectionLevels2.append("SS_IsoRaw_1_5")
selectionLevels2.append("SS_Iso_Medium")
selectionLevels2.append("SS_Iso_Medium")
selectionLevels2.append("MuMedium_SS_Iso_Medium")

referenceLevels = []
referenceLevels.append("SS_NoIso")
referenceLevels.append("SS_NoIso")

referenceLevels2 = []
referenceLevels2.append("SS_InvertIsoRaw_1_5")
referenceLevels2.append("SS_InvertIso_Medium")
referenceLevels2.append("SS_InvertIso_Medium_RawOnly")
referenceLevels2.append("MuMedium_SS_InvertIso_Medium")

names = []
names.append("SS_IsoRaw_1_5_Vs_SS_NoIso")
names.append("SS_Iso_Medium_Vs_SS_NoIso")

names2 = []
names2.append("SS_IsoRaw_1_5_Vs_SS_InvertIsoRaw_1_5")
names2.append("SS_Iso_Medium_Vs_SS_InvertIso_Medium")
names2.append("SS_Iso_Medium_Vs_SS_InvertIso_Medium_RawOnly")
names2.append("MuMedium_SS_Iso_Medium_Vs_MuMedium_SS_InvertIso_Medium")

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

#effPlots = EfficiencyInBinsPlots()
#effPlots.name = name
#effPlots.histoBaseName = "hFakeRate"
#effPlots.inputFileNames = inputFileNames
#effPlots.selectionLevels = selectionLevels
#effPlots.plotInfos = plotInfos
#effPlots.referenceLevels = referenceLevels 
#effPlots.individualNames = names
#effPlots.variables = variables
#effPlots.variableNames = variableNames
#effPlots.variableLegends = variableLegends
#effPlots.variableBins = variableBins
#effPlots.outputFile = outputFile
#effPlots.plot(0., 0.5)
#efficiencyPlots.append(effPlots)

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
