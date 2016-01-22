import ROOT
import os
import copy
from EfficiencyPlots import EfficiencyPlot, PlotInfo

baseDir = '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Studies/FakeRate/ComputeFakeRates/plots/'
ZJets1DFileName = 'FakeFactors_ZMuMu_1D/FakeFactors_ZMuMu_1D.root'
WJets1DFileName = 'FakeFactors_HighMT_1D/FakeFactors_HighMT_1D.root'
ZJetsBinnedFileName = 'FakeFactors_ZMuMu_Binned/FakeFactors_ZMuMu_Binned.root'
WJetsBinnedFileName = 'FakeFactors_HighMT_Binned/FakeFactors_HighMT_Binned.root'

plotDir = 'plots/FakeFactors_ZJetsVsWJets/'

ZJets1DFile = ROOT.TFile.Open(baseDir+ZJets1DFileName)
WJets1DFile = ROOT.TFile.Open(baseDir+WJets1DFileName)
ZJetsBinnedFile = ROOT.TFile.Open(baseDir+ZJetsBinnedFileName)
WJetsBinnedFile = ROOT.TFile.Open(baseDir+WJetsBinnedFileName)


ZJets1D_VsJetPt = ZJets1DFile.Get('FakeFactors_ZMuMu_1D_Iso_Medium_InvertIso_Medium_tau_jet_pt')
ZJets1D_VsJetPt.__class__ = ROOT.TGraphAsymmErrors
WJets1D_VsJetPt = WJets1DFile.Get('FakeFactors_HighMT_1D_Iso_Medium_InvertIso_Medium_tau_jet_pt')
WJets1D_VsJetPt.__class__ = ROOT.TGraphAsymmErrors
#
ZJets1D_VsPdgId = ZJets1DFile.Get('FakeFactors_ZMuMu_1D_Iso_Medium_InvertIso_Medium_tau_pdgId')
ZJets1D_VsPdgId.__class__ = ROOT.TGraphAsymmErrors
WJets1D_VsPdgId = WJets1DFile.Get('FakeFactors_HighMT_1D_Iso_Medium_InvertIso_Medium_tau_pdgId')
WJets1D_VsPdgId.__class__ = ROOT.TGraphAsymmErrors
#
ZJetsBinned_VsJetPt_Decay = []
WJetsBinned_VsJetPt_Decay = []
for decay in xrange(3):
    ZJetsBinned_VsJetPt_Decay.append(ZJetsBinnedFile.Get('FakeFactors_ZMuMu_Binned_Iso_Medium_InvertIso_Medium_tau_jet_pt_vs_decayMode_{DECAY}'.format(DECAY=decay)))
    ZJetsBinned_VsJetPt_Decay[-1].__class__ = ROOT.TGraphAsymmErrors
    WJetsBinned_VsJetPt_Decay.append(WJetsBinnedFile.Get('FakeFactors_HighMT_Binned_Iso_Medium_InvertIso_Medium_tau_jet_pt_vs_decayMode_{DECAY}'.format(DECAY=decay)))
    WJetsBinned_VsJetPt_Decay[-1].__class__ = ROOT.TGraphAsymmErrors


plotInfoWJets = PlotInfo()
plotInfoWJets.markerStyle = 24
plotInfoWJets.markerColor = ROOT.kBlack
plotInfoWJets.lineColor = ROOT.kBlack
plotInfoWJets.legend = 'W+jet, m_{T}>40GeV'
plotInfoWJets.yTitle = 'Fake factor'
#
plotInfoZJets = PlotInfo()
plotInfoZJets.markerStyle = 20
plotInfoZJets.markerColor = ROOT.kBlack
plotInfoZJets.lineColor = ROOT.kBlack
plotInfoZJets.legend = 'Z+jet'
plotInfoZJets.yTitle = 'Fake factor'

def updateXTitle(plotInfo, xTitle):
    infoCopy = copy.copy(plotInfo)
    infoCopy.xTitle = xTitle
    return infoCopy

plots = []
#
plots.append(EfficiencyPlot())
plots[-1].plotDir = plotDir
plots[-1].name = 'FakeFactors_Iso_Medium_Vs_InvertIso_Medium_ZJetsVsWJets_tau_jet_pt'
plots[-1].drawLegend = True
plots[-1].legendPosition = [0.6, 0.7, 0.95, 0.9] 
plots[-1].addGraph(WJets1D_VsJetPt, updateXTitle(plotInfoWJets, 'p_{T}^{jet} [GeV]'))
plots[-1].addGraph(ZJets1D_VsJetPt, updateXTitle(plotInfoZJets, 'p_{T}^{jet} [GeV]'))
plots[-1].plot(0., 0.3)
#
plots.append(EfficiencyPlot())
plots[-1].plotDir = plotDir
plots[-1].name = 'FakeFactors_Iso_Medium_Vs_InvertIso_Medium_ZJetsVsWJets_tau_pdgId'
plots[-1].drawLegend = True
plots[-1].legendPosition = [0.6, 0.7, 0.95, 0.9] 
plots[-1].addGraph(WJets1D_VsPdgId, updateXTitle(plotInfoWJets, '|pdg ID| #times sign-flip'))
plots[-1].addGraph(ZJets1D_VsPdgId, updateXTitle(plotInfoZJets, '|pdg ID| #times sign-flip'))
plots[-1].plot(0., 0.3)
#
for decay in xrange(3):
    plots.append(EfficiencyPlot())
    plots[-1].plotDir = plotDir
    plots[-1].name = 'FakeFactors_Iso_Medium_Vs_InvertIso_Medium_ZJetsVsWJets_decay{DECAY}_tau_jet_pt'.format(DECAY=decay)
    plots[-1].drawLegend = True
    plots[-1].legendPosition = [0.6, 0.7, 0.95, 0.9] 
    plots[-1].addGraph(WJetsBinned_VsJetPt_Decay[decay], updateXTitle(plotInfoWJets, 'p_{T}^{jet} [GeV]'))
    plots[-1].addGraph(ZJetsBinned_VsJetPt_Decay[decay], updateXTitle(plotInfoZJets, 'p_{T}^{jet} [GeV]'))
    plots[-1].plot(0., 0.5)

