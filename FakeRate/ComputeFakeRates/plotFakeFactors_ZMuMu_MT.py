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


inputFileName = "../../../Histos/StudyFakeRate/MuMu_MTStudy/Z/v_1_2016-01-27/fakerates_ZMuMu_MTStudy_Z.root"
plotDir = "plots/"
name = "FakeFactors_ZMuMu_MT"

systems = []
systems.append("")

selectionLevels = []
selectionLevels.append(("Iso_Medium",))


referenceLevels = []
referenceLevels.append(("InvertIso_Medium",))

names = []
names.append("Iso_Medium_Vs_InvertIso_Medium")


variables = ["mt"]
variableNames = {}
variableNames["mt"] = "m_{T} [GeV]"



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
effPlots.rebin = 2
effPlots.plot(0., 0.3)
efficiencyPlots.append(effPlots)


outputFile.Close()
