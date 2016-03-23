import ROOT
import os
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


inputFileNames = [
    ["../../../Histos/StudyFakeRate/MuTau_FakeRateWJetsHighMT/Data_Run15D_v4/v_3_2016-01-29/fakerates_MuTau_WJetsHighMT_Data_Run15D_v4.root",1],
    ["../../../Histos/StudyFakeRate/MuTau_FakeRateWJetsHighMT/Data_Run15D_05Oct/v_3_2016-01-29/fakerates_MuTau_WJetsHighMT_Data_Run15D_05Oct.root",1],
]
plotDir = "plots/"
name = "FakeFactors_Data_HighMT_1D"
systems = []
systems.append("")

selectionLevels = []
selectionLevels.append(("IsoRaw_1_5",))
selectionLevels.append(("Iso_Medium",))

selectionLevels2 = []
selectionLevels2.append(("IsoRaw_1_5",))
selectionLevels2.append(("Iso_Medium",))
selectionLevels2.append(("Iso_Medium",))

referenceLevels = []
referenceLevels.append(("NoIso",))
referenceLevels.append(("NoIso",))

referenceLevels2 = []
referenceLevels2.append(("InvertIsoRaw_1_5",))
referenceLevels2.append(("InvertIso_Medium",))
referenceLevels2.append(("InvertIso_Medium_RawOnly",))

names = []
names.append("IsoRaw_1_5_Vs_NoIso")
names.append("Iso_Medium_VsNoIso")

names2 = []
names2.append("IsoRaw_1_5_Vs_InvertIsoRaw_1_5")
names2.append("Iso_Medium_Vs_InvertIso_Medium")
names2.append("Iso_Medium_Vs_InvertIso_Medium_RawOnly")

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

effPlots = EfficiencyPlots()
effPlots.name = name
effPlots.publicationDir = publicationDir
effPlots.histoBaseName = "hFakeRate"
effPlots.inputFileNames = [inputFileNames]
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
