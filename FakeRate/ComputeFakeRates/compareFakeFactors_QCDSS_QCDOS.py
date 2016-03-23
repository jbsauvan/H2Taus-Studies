import ROOT
import os
import copy
from EfficiencyPlots import EfficiencyPlot, PlotInfo

baseDir = '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Studies/FakeRate/ComputeFakeRates/plots/'
QCDSS1DFileName = 'FakeFactors_Data_QCDSS_1D/FakeFactors_Data_QCDSS_1D.root'
QCDOS1DFileName = 'FakeFactors_Data_QCDOS_1D/FakeFactors_Data_QCDOS_1D.root'
QCDSSBinnedFileName = 'FakeFactors_Data_QCDSS_Binned/FakeFactors_Data_QCDSS_Binned.root'
QCDOSBinnedFileName = 'FakeFactors_Data_QCDOS_Binned/FakeFactors_Data_QCDOS_Binned.root'

plotDir = 'plots/FakeFactors_QCDSS_Vs_QCDOS/'

QCDSS1DFile = ROOT.TFile.Open(baseDir+QCDSS1DFileName)
QCDOS1DFile = ROOT.TFile.Open(baseDir+QCDOS1DFileName)
QCDSSBinnedFile = ROOT.TFile.Open(baseDir+QCDSSBinnedFileName)
QCDOSBinnedFile = ROOT.TFile.Open(baseDir+QCDOSBinnedFileName)


QCDSS1D_VsPt = QCDSS1DFile.Get('FakeFactors_Data_QCDSS_1D_SS_Iso_Medium_SS_InvertIso_Medium_tau_pt')
QCDSS1D_VsPt.__class__ = ROOT.TGraphAsymmErrors
QCDOS1D_VsPt = QCDOS1DFile.Get('FakeFactors_Data_QCDOS_1D_Iso_Medium_InvertIso_Medium_tau_pt')
QCDOS1D_VsPt.__class__ = ROOT.TGraphAsymmErrors
#
QCDSS1D_VsDecay = QCDSS1DFile.Get('FakeFactors_Data_QCDSS_1D_SS_Iso_Medium_SS_InvertIso_Medium_tau_decayMode')
QCDSS1D_VsDecay.__class__ = ROOT.TGraphAsymmErrors
QCDOS1D_VsDecay = QCDOS1DFile.Get('FakeFactors_Data_QCDOS_1D_Iso_Medium_InvertIso_Medium_tau_decayMode')
QCDOS1D_VsDecay.__class__ = ROOT.TGraphAsymmErrors
#
QCDSSBinned_VsPt_Decay = []
QCDOSBinned_VsPt_Decay = []
for decay in xrange(3):
    QCDSSBinned_VsPt_Decay.append(QCDSSBinnedFile.Get('FakeFactors_Data_QCDSS_Binned_SS_Iso_Medium_SS_InvertIso_Medium_tau_pt_vs_decayMode_{DECAY}'.format(DECAY=decay)))
    QCDSSBinned_VsPt_Decay[-1].__class__ = ROOT.TGraphAsymmErrors
    QCDOSBinned_VsPt_Decay.append(QCDOSBinnedFile.Get('FakeFactors_Data_QCDOS_Binned_Iso_Medium_InvertIso_Medium_tau_pt_vs_decayMode_{DECAY}'.format(DECAY=decay)))
    QCDOSBinned_VsPt_Decay[-1].__class__ = ROOT.TGraphAsymmErrors


plotInfoQCDOS = PlotInfo()
plotInfoQCDOS.markerStyle = 24
plotInfoQCDOS.markerColor = ROOT.kBlack
plotInfoQCDOS.lineColor = ROOT.kBlack
plotInfoQCDOS.legend = 'iso(#mu)>0.15, OS'
plotInfoQCDOS.yTitle = 'Fake factor'
#
plotInfoQCDSS = PlotInfo()
plotInfoQCDSS.markerStyle = 20
plotInfoQCDSS.markerColor = ROOT.kBlack
plotInfoQCDSS.lineColor = ROOT.kBlack
plotInfoQCDSS.legend = 'iso(#mu)>0.15, SS'
plotInfoQCDSS.yTitle = 'Fake factor'

def updateXTitle(plotInfo, xTitle):
    infoCopy = copy.copy(plotInfo)
    infoCopy.xTitle = xTitle
    return infoCopy

plots = []
#
plots.append(EfficiencyPlot())
plots[-1].plotDir = plotDir
plots[-1].name = 'FakeFactors_Iso_Medium_Vs_InvertIso_Medium_QCDSS_Vs_QCDOS_tau_pt'
plots[-1].drawLegend = True
plots[-1].legendPosition = [0.6, 0.7, 0.95, 0.9] 
plots[-1].addGraph(QCDOS1D_VsPt, updateXTitle(plotInfoQCDOS, 'p_{T}^{#tau} [GeV]'))
plots[-1].addGraph(QCDSS1D_VsPt, updateXTitle(plotInfoQCDSS, 'p_{T}^{#tau} [GeV]'))
plots[-1].plot(0., 0.3)
#
plots.append(EfficiencyPlot())
plots[-1].plotDir = plotDir
plots[-1].name = 'FakeFactors_Iso_Medium_Vs_InvertIso_Medium_QCDSS_Vs_QCDOS_tau_decayMode'
plots[-1].drawLegend = True
plots[-1].legendPosition = [0.6, 0.7, 0.95, 0.9] 
plots[-1].addGraph(QCDOS1D_VsDecay, updateXTitle(plotInfoQCDOS, 'decay mode'))
plots[-1].addGraph(QCDSS1D_VsDecay, updateXTitle(plotInfoQCDSS, 'decay mode'))
plots[-1].plot(0., 0.3)
#
for decay in xrange(3):
    plots.append(EfficiencyPlot())
    plots[-1].plotDir = plotDir
    plots[-1].name = 'FakeFactors_Iso_Medium_Vs_InvertIso_Medium_QCDSSVsQCDOS_decay{DECAY}_tau_pt'.format(DECAY=decay)
    plots[-1].drawLegend = True
    plots[-1].legendPosition = [0.6, 0.2, 0.95, 0.4] 
    plots[-1].addGraph(QCDOSBinned_VsPt_Decay[decay], updateXTitle(plotInfoQCDOS, 'p_{T}^{#tau} [GeV]'))
    plots[-1].addGraph(QCDSSBinned_VsPt_Decay[decay], updateXTitle(plotInfoQCDSS, 'p_{T}^{#tau} [GeV]'))
    plots[-1].plot(0., 0.2)

