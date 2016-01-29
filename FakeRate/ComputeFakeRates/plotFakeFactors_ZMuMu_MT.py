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

if not os.path.exists(plotDir+"/"+name):
    os.makedirs(plotDir+"/"+name)
outputFile = ROOT.TFile.Open(plotDir+"/"+name+"/"+name+".root", "RECREATE")

################################################
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

################################################
systems2 = []
systems2.append("MTlt40")
systems2.append("MTgt70")

selectionLevels2 = []
selectionLevels2.append(("Iso_Medium","Iso_Medium",))


referenceLevels2 = []
referenceLevels2.append(("InvertIso_Medium","InvertIso_Medium",))

names2 = []
names2.append("Iso_Medium_Vs_InvertIso_Medium")


variables2 = ["nevents", 'tau_pt', 'tau_decayMode']
variableNames2 = {}
variableNames2["nevents"] = ""
variableNames2["tau_pt"] = "p_{T}^{#tau} [GeV]"
variableNames2["tau_decayMode"] = "decayMode"



plotInfos2 = [PlotInfo(),PlotInfo()]
plotInfos2[0].markerStyle = 20
plotInfos2[0].yTitle = "Fake factor" 
plotInfos2[0].legend = 'm_{T}<40GeV'
plotInfos2[1].markerStyle = 24
#plotInfos2[1].markerColor = ROOT.kRed
plotInfos2[1].yTitle = "Fake factor" 
plotInfos2[1].legend = 'm_{T}>70GeV'



effPlots2 = EfficiencyPlots()
effPlots2.name = name
effPlots2.publicationDir = publicationDir
effPlots2.histoBaseName = "hFakeRate"
effPlots2.inputFileNames = [inputFileName]*2
effPlots2.systems = systems2
effPlots2.selectionLevels = selectionLevels2
effPlots2.plotInfos = plotInfos2
effPlots2.referenceLevels = referenceLevels2
effPlots2.individualNames = names2
effPlots2.variables = variables2
effPlots2.variableNames = variableNames2
effPlots2.outputFile = outputFile
effPlots2.divideOption = "pois"
#effPlots2.rebin = 2
effPlots2.plot(0., 0.3)
efficiencyPlots.append(effPlots2)


outputFile.Close()
