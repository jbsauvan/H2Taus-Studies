import ROOT
import os
from EfficiencyPlots import EfficiencyPlots, PlotInfo

publish = False
publicationDir = ""
#if publish:
    #if os.path.exists("/afs/cern.ch/user/j/jsauvan/www/"):
        #publicationDir = "/afs/cern.ch/user/j/jsauvan/www/H2Taus/FakeRate/FakeFactors/"
    #elif os.path.exists("/home/sauvan/lxplus/www/"):
        #publicationDir = "/home/sauvan/lxplus/www/H2Taus/FakeRate/FakeFactors/"
    #else:
        #publish = False


inputFileName = "../../../Histos/StudyFakeRate/MuTau_WJets/W/v_1_2016-01-07/fakerates_MuTau_WJets_W.root"
plotDir = "plots/"
name = "FakeFactors_WJets"
systems = []
systems.append("")


selectionLevels = []
selectionLevels.append(("Iso_Medium_OS",))
selectionLevels.append(("Iso_Medium_SS",))


referenceLevels = []
referenceLevels.append(("InvertIso_Medium_OS",))
referenceLevels.append(("InvertIso_Medium_SS",))

names = []
names.append("Iso_Medium_OS_Vs_InvertIso_Medium_OS")
names.append("Iso_Medium_SS_Vs_InvertIso_Medium_SS")

variables = ["tau_pt_vs_mt_0", "tau_pdgId_vs_mt_0", "tau_pt_vs_mt_1", "tau_pdgId_vs_mt_1", "tau_pt_vs_mt_2", "tau_pdgId_vs_mt_2"]
variableNames = {}
for var in variables:
    if 'tau_pt' in var: variableNames[var] = "p_{T}^{#tau} [GeV]"
    if 'tau_pdgId' in var: variableNames[var] = "|pdg ID| #times sign-flip"



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
effPlots.inputFileNames = [inputFileName]
effPlots.systems = systems
effPlots.selectionLevels = selectionLevels
effPlots.plotInfos = plotInfos
effPlots.referenceLevels = referenceLevels 
effPlots.individualNames = names
effPlots.variables = variables
effPlots.variableNames = variableNames
effPlots.outputFile = outputFile
effPlots.divideOption = "pois"
effPlots.plot(0., 0.5)
efficiencyPlots.append(effPlots)


outputFile.Close()
