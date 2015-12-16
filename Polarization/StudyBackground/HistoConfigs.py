import ROOT
from ComparisonPlot import Config

## MT comparison
configLowMT = Config()
configLowMT.color = ROOT.kBlack
configLowMT.markerStyle = 20
configLowMT.legend = "M_{T} < 40 GeV"

configHighMT = Config()
configHighMT.color = ROOT.kRed-4
configHighMT.markerStyle = 24
configHighMT.legend = "M_{T} > 40 GeV"

## Background comparison
configBackgrounds = {}
configBackgrounds['W'] = Config()
configBackgrounds['W'].color = ROOT.kBlack
configBackgrounds['W'].markerStyle = 20
configBackgrounds['W'].legend = "W+jets"
#
configBackgrounds['QCD'] = Config()
configBackgrounds['QCD'].color = ROOT.kBlue-4
configBackgrounds['QCD'].markerStyle = 25
configBackgrounds['QCD'].legend = "QCD"
#
configBackgrounds['TT'] = Config()
configBackgrounds['TT'].color = ROOT.kRed-4
configBackgrounds['TT'].markerStyle = 26
configBackgrounds['TT'].legend = "t#bar{t}"


## Isolation comparison
configInvertIso = Config()
configInvertIso.color = ROOT.kRed-4
configInvertIso.lineStyle = 1
configInvertIso.lineWidth = 2
configInvertIso.plotCfg = "HIST"
configInvertIso.legend = "Anti-iso"

configIso = Config()
configIso.color = ROOT.kBlack
configIso.markerStyle = 20
configIso.legend = "Iso"
