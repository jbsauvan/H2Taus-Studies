import ROOT
from ComparisonPlot import Config

configZMuMu = Config()
configZMuMu.color = ROOT.kRed
configZMuMu.lineStyle = 1
configZMuMu.lineWidth = 2
configZMuMu.plotCfg = "HIST"
configZMuMu.legend = "Z#rightarrow#mu#mu + X"

configMuTau = Config()
configMuTau.color = ROOT.kBlack
configMuTau.markerStyle = 20
configMuTau.legend = "#mu#tau selection"
