import ROOT
import os
import pickle
from EfficiencyPlots import EfficiencyPlots, PlotInfo

publish = False
publicationDir = ""
if publish:
    if os.path.exists("/afs/cern.ch/user/j/jsauvan/www/"):
        publicationDir = "/afs/cern.ch/user/j/jsauvan/www/H2Taus/FakeRate/FakeFactors/"
    elif os.path.exists("/home/sauvan/lxplus/www/"):
        publicationDir = "/home/sauvan/lxplus/www/H2Taus/FakeRate/FakeFactors/"
    else:
        publish = False

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
name = "FakeFactors_Data_QCDSS_1D"
systems = []
systems.append("")

selectionLevels = []
selectionLevels.append(("SS_IsoRaw_1_5",))
selectionLevels.append(("SS_Iso_Medium",))

selectionLevels2 = []
selectionLevels2.append(("SS_IsoRaw_1_5",))
selectionLevels2.append(("SS_Iso_Medium",))
selectionLevels2.append(("SS_Iso_Medium",))
selectionLevels2.append(("MuMedium_SS_Iso_Medium",))

referenceLevels = []
referenceLevels.append(("SS_NoIso",))
referenceLevels.append(("SS_NoIso",))

referenceLevels2 = []
referenceLevels2.append(("SS_InvertIsoRaw_1_5",))
referenceLevels2.append(("SS_InvertIso_Medium",))
referenceLevels2.append(("SS_InvertIso_Medium_RawOnly",))
referenceLevels2.append(("MuMedium_SS_InvertIso_Medium",))

names = []
names.append("SS_IsoRaw_1_5_Vs_SS_NoIso")
names.append("SS_Iso_Medium_Vs_SS_NoIso")

names2 = []
names2.append("SS_IsoRaw_1_5_Vs_SS_InvertIsoRaw_1_5")
names2.append("SS_Iso_Medium_Vs_SS_InvertIso_Medium")
names2.append("SS_Iso_Medium_Vs_SS_InvertIso_Medium_RawOnly")
names2.append("MuMedium_SS_Iso_Medium_Vs_MuMedium_SS_InvertIso_Medium")

variables = ["tau_pt", "tau_eta", "tau_decayMode", "tau_pdgId", "nevents", "tau_jet_pt"]
variableNames = {}
variableNames["tau_pt"] = "p_{T}^{#tau} [GeV]"
variableNames["tau_eta"] = "#eta^{#tau}"
variableNames["tau_decayMode"] = "decayMode"
variableNames["tau_pdgId"] = "|pdg ID| #times sign-flip"
variableNames["nevents"] = ""
variableNames["nvertices"] = "N_{PV}"
variableNames["rho"] = "#rho"
variableNames["tau_jet_pt"] = "p_{T}^{jet} [GeV]"



plotInfos = [PlotInfo()]
plotInfos[0].markerStyle = 20
plotInfos[0].yTitle = "Fake factor" 

if not os.path.exists(plotDir+"/"+name):
    os.makedirs(plotDir+"/"+name)
outputFile = ROOT.TFile.Open(plotDir+"/"+name+"/"+name+".root", "RECREATE")

efficiencyPlots = []

#effPlots = EfficiencyPlots()
#effPlots.name = name
#effPlots.publicationDir = publicationDir
#effPlots.histoBaseName = "hFakeRate"
#effPlots.inputFileNames = [inputFileNames]
#effPlots.systems = systems
#effPlots.selectionLevels = selectionLevels
#effPlots.plotInfos = plotInfos
#effPlots.referenceLevels = referenceLevels 
#effPlots.individualNames = names
#effPlots.variables = variables
#effPlots.variableNames = variableNames
#effPlots.outputFile = outputFile
#effPlots.plot(0., 0.5)
#efficiencyPlots.append(effPlots)

effPlots = EfficiencyPlots()
effPlots.name = name
effPlots.publicationDir = publicationDir
effPlots.histoBaseName = "hFakeRate"
effPlots.inputFileNames = [inputFileNames]
effPlots.systems = systems
effPlots.selectionLevels = selectionLevels2
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
