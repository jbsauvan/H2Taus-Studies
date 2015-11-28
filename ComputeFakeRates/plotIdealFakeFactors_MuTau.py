import ROOT
import os
from EfficiencyPlots import EfficiencyPlots, PlotInfo



inputFileName = "../../Histos/StudyFakeRate/MuTau/W/v_5_2015-11-25/fakerates_MuTau_W.root"
plotDir = "plots/"
name = "IdealFakeFactors_MuTau"
systems = []
systems.append("")

selectionLevels = []
selectionLevels.append(("StandardIso",))

referenceLevels = []
referenceLevels.append(("NoIso",))

referenceLevels2 = []
referenceLevels2.append(("InvertIso",))

names = []
names.append("VsNoIso")

names2 = []
names2.append("VsInvertIso")

variables = ["mvis_vs_match5"]
variableNames = {}
variableNames["mvis_vs_match5"] = "M_{vis} [GeV]"



plotInfos = [PlotInfo()]
plotInfos[0].markerStyle = 20
plotInfos[0].yTitle = "Fake factor" 

if not os.path.exists(plotDir+"/"+name):
    os.makedirs(plotDir+"/"+name)
outputFile = ROOT.TFile.Open(plotDir+"/"+name+"/"+name+".root", "RECREATE")

efficiencyPlots = []

effPlots = EfficiencyPlots()
effPlots.name = name
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
effPlots.plot(0., 0.5)
efficiencyPlots.append(effPlots)

effPlots = EfficiencyPlots()
effPlots.name = name
effPlots.histoBaseName = "hFakeRate"
effPlots.inputFileNames = [inputFileName]
effPlots.systems = systems
effPlots.selectionLevels = selectionLevels
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
