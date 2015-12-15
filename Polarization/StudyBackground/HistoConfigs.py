import ROOT
from ComparisonPlot import Config

## MT comparison
configLowMT = Config()
configLowMT.color = ROOT.kRed
configLowMT.lineStyle = 1
configLowMT.lineWidth = 2
configLowMT.plotCfg = "HIST"
configLowMT.legend = "M_{T} < 40 GeV"

configHighMT = Config()
configHighMT.color = ROOT.kBlack
configHighMT.markerStyle = 20
configHighMT.legend = "M_{T} > 40 GeV"

## Background comparison
configBackgrounds = {}
configBackgrounds['W'] = Config()
configBackgrounds['W'].color = ROOT.kRed
configBackgrounds['W'].lineStyle = 1
configBackgrounds['W'].markerStyle = 20
configBackgrounds['W'].lineWidth = 1
#configBackgrounds['W'].plotCfg = "HIST"
configBackgrounds['W'].legend = "W+jets"
#
configBackgrounds['QCD'] = Config()
configBackgrounds['QCD'].color = ROOT.kBlue
configBackgrounds['QCD'].lineStyle = 1
configBackgrounds['QCD'].markerStyle = 25
configBackgrounds['QCD'].lineWidth = 1
#configBackgrounds['QCD'].plotCfg = "HIST"
configBackgrounds['QCD'].legend = "QCD"
#
configBackgrounds['TT'] = Config()
configBackgrounds['TT'].color = ROOT.kMagenta
configBackgrounds['TT'].lineStyle = 1
configBackgrounds['TT'].markerStyle = 26
configBackgrounds['TT'].lineWidth = 1
#configBackgrounds['TT'].plotCfg = "HIST"
configBackgrounds['TT'].legend = "t#bar{t}"


## Isolation comparison
configInvertIso = Config()
configInvertIso.color = ROOT.kRed
configInvertIso.lineStyle = 1
configInvertIso.lineWidth = 2
configInvertIso.plotCfg = "HIST"
configInvertIso.legend = "Anti-iso"

configIso = Config()
configIso.color = ROOT.kBlack
configIso.markerStyle = 20
configIso.legend = "Iso"
