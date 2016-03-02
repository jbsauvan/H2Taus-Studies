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


inputFileName = "../../../Histos/StudyFakeRate/MuMu_MTStudy/76X/Z/v_1_2016-03-01/fakerates_ZMuMu_MTStudy_Z.root"
plotDir = "plots/"
name = "FakeFactors_ZMuMu_HighMT_1D"
systems = []
systems.append("")

selectionLevels2 = []
selectionLevels2.append(("MTgt70_Iso_Medium",))


referenceLevels2 = []
referenceLevels2.append(("MTgt70_InvertIso_Medium",))


names2 = []
names2.append("Iso_Medium_Vs_InvertIso_Medium")

variables = ["tau_pt",  "tau_decayMode"]
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
effPlots.inputFileNames = [[inputFileName]]
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
