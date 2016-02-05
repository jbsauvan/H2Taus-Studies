import ROOT
import os
from EfficiencyPlots import EfficiencyPlots, EfficiencyInBinsPlots, PlotInfo

publish = False
publicationDir = ""
#if publish:
    #if os.path.exists("/afs/cern.ch/user/j/jsauvan/www/"):
        #publicationDir = "/afs/cern.ch/user/j/jsauvan/www/H2Taus/FakeRate/FakeFactors/"
    #elif os.path.exists("/home/sauvan/lxplus/www/"):
        #publicationDir = "/home/sauvan/lxplus/www/H2Taus/FakeRate/FakeFactors/"
    #else:
        #publish = False


#inputFileName = "../../../Histos/StudyFakeRate/MuTau_WJets/W/v_5_2016-01-28/fakerates_MuTau_WJets_W.root"
inputFileName = "../../../Histos/StudyFakeRate/MuTau_WJets/W/v_4_2016-01-15/fakerates_MuTau_WJets_W.root"
plotDir = "plots/"
name = "FakeFactors_WJets"
systems = []
systems.append("")


selectionLevels = []
selectionLevels.append("Iso_Medium_OS")
selectionLevels.append("Iso_Medium_SS")
selectionLevels.append("Iso_Medium_OS")
selectionLevels.append("Iso_Medium_OS")


referenceLevels = []
referenceLevels.append("InvertIso_Medium_OS")
referenceLevels.append("InvertIso_Medium_SS")
referenceLevels.append("Loose10InvertIso_Medium_OS")
referenceLevels.append("Loose20InvertIso_Medium_OS")

names = []
names.append("Iso_Medium_OS_Vs_InvertIso_Medium_OS")
names.append("Iso_Medium_SS_Vs_InvertIso_Medium_SS")
names.append("Iso_Medium_OS_Vs_Loose10InvertIso_Medium_OS")
names.append("Iso_Medium_OS_Vs_Loose20InvertIso_Medium_OS")

variables = ["tau_pt_vs_mt_", "tau_pdgId_vs_mt_", "muon_pt_vs_mt_", "met_pt_vs_mt_", "muon_iso_vs_mt_", "delta_phi_muon_met_vs_mt_", "delta_phi_tau_met_vs_mt_", "tau_gen_pt_vs_mt_", "tau_jet_pt_vs_mt_"]
variableNames = {}
for var in variables:
    if 'tau_pt' in var: variableNames[var] = "p_{T}^{#tau} [GeV]"
    if 'tau_pdgId' in var: variableNames[var] = "|pdg ID| #times sign-flip"
    if 'muon_pt' in var: variableNames[var] = "p_{T}^{#mu} [GeV]"
    if 'muon_iso' in var: variableNames[var] = "Muon isolation"
    if 'met_pt' in var: variableNames[var] = "MET [GeV]"
    if 'delta_phi_muon_met_vs_mt_' in var: variableNames[var] = "#Delta#Phi(#mu,MET)"
    if 'delta_phi_tau_met_vs_mt_' in var: variableNames[var] = "#Delta#Phi(#tau,MET)"
    if 'tau_gen_pt' in var: variableNames[var] = "p_{T}^{matched gen parton} [GeV]"
    if 'tau_jet_pt' in var: variableNames[var] = "p_{T}^{matched reco jet} [GeV]"

variableBins = {}
variableLegends = {}
for var in variables:
    variableBins[var] = [0,1,2,3]
    variableLegends[var] = ["M_{T} < 20GeV", "20 < M_{T} < 40GeV","40 < M_{T} < 80GeV","M_{T} > 80GeV"]
#variableBins["tau_pt_vs_mt_"] = [0,1,2,3]
#variableBins["tau_pdgId_vs_mt_"] = [0,1,2,3]
#variableBins["muon_pt_vs_mt_"] = [0,1,2,3]
#variableBins["muon_pt_vs_mt_"] = [0,1,2,3]
#variableBins["muon_iso_vs_mt_"] = [0,1,2,3]
#variableBins["met_pt_vs_mt_"] = [0,1,2,3]


#variableLegends["tau_pt_vs_mt_"] = ["M_{T} < 20GeV", "20 < M_{T} < 40GeV","40 < M_{T} < 80GeV","M_{T} > 80GeV"]
#variableLegends["tau_pdgId_vs_mt_"] = ["M_{T} < 20GeV", "20 < M_{T} < 40GeV","40 < M_{T} < 80GeV","M_{T} > 80GeV"]



colors = [
    ROOT.kBlack,
    ROOT.kBlack,
    ROOT.kRed,
    ROOT.kRed,
]

markers = [
    20,
    24,
    20,
    24,
]


plotInfos = []
for i in xrange(len(colors)):
    plotInfos.append(PlotInfo())
    plotInfos[-1].markerStyle = markers[i]
    plotInfos[-1].markerColor = colors[i]
    plotInfos[-1].lineColor = colors[i]
    plotInfos[-1].yTitle = "Fake factor"


if not os.path.exists(plotDir+"/"+name):
    os.makedirs(plotDir+"/"+name)
outputFile = ROOT.TFile.Open(plotDir+"/"+name+"/"+name+".root", "RECREATE")

efficiencyPlots = []


#effPlots = EfficiencyPlots()
#effPlots.name = name
#effPlots.publicationDir = publicationDir
#effPlots.histoBaseName = "hFakeRate"
#effPlots.inputFileNames = [inputFileName]
#effPlots.systems = systems
#effPlots.selectionLevels = selectionLevels
#effPlots.plotInfos = plotInfos
#effPlots.referenceLevels = referenceLevels 
#effPlots.individualNames = names
#effPlots.variables = variables
#effPlots.variableNames = variableNames
#effPlots.outputFile = outputFile
#effPlots.divideOption = "pois"
#effPlots.plot(0., 0.5)
#efficiencyPlots.append(effPlots)

effPlots = EfficiencyInBinsPlots()
effPlots.name = name
effPlots.histoBaseName = "hFakeRate"
effPlots.inputFileName = inputFileName
effPlots.selectionLevels = selectionLevels
effPlots.plotInfos = plotInfos
effPlots.referenceLevels = referenceLevels 
effPlots.individualNames = names
effPlots.variables = variables
effPlots.variableNames = variableNames
effPlots.variableLegends = variableLegends
effPlots.variableBins = variableBins
effPlots.outputFile = outputFile
effPlots.divideOption = "pois"
effPlots.plot(0., 0.3)
efficiencyPlots.append(effPlots)


########################################################

systems = []
systems.append("")

selectionLevels = []
selectionLevels.append(("Iso_Medium_OS",))
selectionLevels.append(("Iso_Medium_SS",))
selectionLevels.append(("Iso_Medium_OS",))
selectionLevels.append(("Iso_Medium_OS",))


referenceLevels = []
referenceLevels.append(("InvertIso_Medium_OS",))
referenceLevels.append(("InvertIso_Medium_SS",))
referenceLevels.append(("Loose10InvertIso_Medium_OS",))
referenceLevels.append(("Loose20InvertIso_Medium_OS",))

names = []
names.append("Iso_Medium_OS_Vs_InvertIso_Medium_OS")
names.append("Iso_Medium_SS_Vs_InvertIso_Medium_SS")
names.append("Iso_Medium_OS_Vs_Loose10InvertIso_Medium_OS")
names.append("Iso_Medium_OS_Vs_Loose20InvertIso_Medium_OS")


variables = ["mt", 'mt_gen']
variableNames = {}
variableNames["mt"] = "m_{T} [GeV]"
variableNames["mt_gen"] = "m_{T}^{gen} [GeV]"



plotInfos = [PlotInfo()]
plotInfos[0].markerStyle = 20
plotInfos[0].yTitle = "Fake factor" 

if not os.path.exists(plotDir+"/"+name):
    os.makedirs(plotDir+"/"+name)
outputFile = ROOT.TFile.Open(plotDir+"/"+name+"/"+name+".root", "RECREATE")


effPlots2 = EfficiencyPlots()
effPlots2.name = name
effPlots2.publicationDir = publicationDir
effPlots2.histoBaseName = "hFakeRate"
effPlots2.inputFileNames = [[inputFileName]]
effPlots2.systems = systems
effPlots2.selectionLevels = selectionLevels
effPlots2.plotInfos = plotInfos
effPlots2.referenceLevels = referenceLevels 
effPlots2.individualNames = names
effPlots2.variables = variables
effPlots2.variableNames = variableNames
effPlots2.outputFile = outputFile
effPlots2.divideOption = "pois"
effPlots2.rebin = 2
effPlots2.plot(0., 0.3)
efficiencyPlots.append(effPlots2)


outputFile.Close()
