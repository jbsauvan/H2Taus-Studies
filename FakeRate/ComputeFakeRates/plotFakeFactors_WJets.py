import ROOT
import os
from EfficiencyPlots import EfficiencyPlots, EfficiencyInBinsPlots, PlotInfo
from array import array
import math

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
effPlots.inputFileNames = [inputFileName]
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
effPlots2.rebin = [0.,10.,20.,30.,40.,50.,60.,70.,200.]
effPlots2.plot(0., 0.3)
efficiencyPlots.append(effPlots2)



########################################################
## Compute corrections for mT>70GeV corrections


def graphDivide(graph1, graph2):
    x = []
    y = []
    xe = []
    ye = []
    for p in range(0, graph1.GetN()):
        x.append(graph1.GetX()[p])
        xe.append((graph1.GetEXlow()[p]+graph1.GetEXhigh()[p])/2.)
        y1p = graph1.GetY()[p]
        y2p = graph2.GetY()[p]
        ye1p = (graph1.GetEYlow()[p]+graph1.GetEYhigh()[p])/2.
        ye2p = (graph2.GetEYlow()[p]+graph2.GetEYhigh()[p])/2.
        if y2p!=0. and y2p**2!=0.:
            y.append(y1p / y2p)
            ye.append(math.sqrt( (ye1p/y2p)**2 + (ye2p*y1p/y2p**2)**2 ))
        else:
            y.append(0.)
            ye.append(0.)
    print y
    graph = ROOT.TGraphAsymmErrors(len(x), array('d',x), array('d',y), array('d',xe), array('d',xe), array('d',ye), array('d',ye))
    graph.SetName(graph1.GetName()+"_div")
    return graph

outputFileCorr = ROOT.TFile.Open(plotDir+"/"+name+"/"+name+"_highMTCorrections.root", "RECREATE")

fakeFactorVsMT = outputFile.Get('FakeFactors_WJets_Iso_Medium_OS_InvertIso_Medium_OS_mt')
highMTFactor = fakeFactorVsMT.GetY()[fakeFactorVsMT.GetN()-1]
highMTFactorErrorLow = fakeFactorVsMT.GetEYlow()[fakeFactorVsMT.GetN()-1]
highMTFactorErrorHigh = fakeFactorVsMT.GetEYhigh()[fakeFactorVsMT.GetN()-1]
xs = []
xslow = []
xshigh = []
ys = []
yslow = []
yshigh = []
for p in xrange(fakeFactorVsMT.GetN()):
    xs.append(fakeFactorVsMT.GetX()[p])
    xslow.append(fakeFactorVsMT.GetEXlow()[p])
    xshigh.append(fakeFactorVsMT.GetEXhigh()[p])
    ys.append(highMTFactor)
    yslow.append(highMTFactorErrorLow)
    yshigh.append(highMTFactorErrorHigh)
highMTGraph = ROOT.TGraphAsymmErrors(len(xs), array('d',xs), array('d',ys), array('d',xslow), array('d',xshigh), array('d',yslow), array('d',yshigh))
correctionGraph = graphDivide(fakeFactorVsMT, highMTGraph)
correctionGraph.SetPointEYlow(correctionGraph.GetN()-1, 0)
correctionGraph.SetPointEYhigh(correctionGraph.GetN()-1, 0)
correctionGraph.SetName('HighMTCorrection_WJets_Iso_Medium_OS_InvertIso_Medium_OS_mt')
correctionGraph.Write()

canvas = ROOT.TCanvas('canvas', 'canvas', 800, 800)
hDummy = ROOT.TH1F('hDummy', 'hDummy', 1, 0, 200)
corrs = correctionGraph.GetY()
corrs.SetSize(correctionGraph.GetN())
maxi = max(corrs)*1.1
mini = 0
hDummy.SetAxisRange(mini,maxi)
hDummy.SetXTitle('m_{T} [GeV]')
hDummy.SetYTitle('Correction')
hDummy.Draw()
correctionGraph.SetMarkerStyle(20)
correctionGraph.Draw('p same')
canvas.Print(plotDir+"/"+name+"/"+name+"_highMTCorrections.png")


outputFile.Close()
outputFileCorr.Close()
