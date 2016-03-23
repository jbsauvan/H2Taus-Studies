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


inputFileName = ["../../../Histos/StudyFakeRate/MuMu_MTStudy/Z/v_4_2016-02-02/fakerates_ZMuMu_MTStudy_Z.root",1]
plotDir = "plots/FakeFactors_ZMuMu_MT/"

muon2PtCuts = [6,7,8,9,10,12,14,16,18,20]
directories = ['Muon2PtCut_{CUT}/'.format(CUT=cut) for cut in muon2PtCuts]
directories.append('')

if not os.path.exists(plotDir):
    os.makedirs(plotDir)
outputFile = ROOT.TFile.Open(plotDir+"/FakeFactors_ZMuMu_MT.root", "RECREATE")

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

for directory in directories:
    #namesCopy = []
    #for n in names:
        #namesCopy.append('{DIR}{NAME}'.format(DIR=directory.replace('/','_'),NAME=n))
    effPlots = EfficiencyPlots()
    effPlots.plotDir = plotDir
    effPlots.name = '{DIR}'.format(DIR=directory.replace('/',''))
    if effPlots.name=='': effPlots.name = 'Muon2PtCut_5'
    effPlots.publicationDir = publicationDir
    effPlots.histoBaseName = "{DIR}hFakeRate".format(DIR=directory)
    effPlots.inputFileNames = [[inputFileName]]
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



for directory in directories:
    #namesCopy = []
    #for n in names2:
        #namesCopy.append('{DIR}{NAME}'.format(DIR=directory.replace('/','_'),NAME=n))
    effPlots2 = EfficiencyPlots()
    effPlots2.plotDir = plotDir
    effPlots2.name = '{DIR}'.format(DIR=directory.replace('/',''))
    if effPlots2.name=='': effPlots2.name = 'Muon2PtCut_5'
    effPlots2.publicationDir = publicationDir
    effPlots2.histoBaseName = "{DIR}hFakeRate".format(DIR=directory)
    effPlots2.inputFileNames = [[inputFileName]]*2
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
