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


### W+jets study
configMTbins = []
configMTbins.append(Config())
configMTbins[-1].color = ROOT.kBlack
configMTbins[-1].lineStyle = 1
configMTbins[-1].lineWidth = 2
configMTbins[-1].plotCfg = "HIST"
configMTbins[-1].legend = "M_{T} < 40GeV"
#
configMTbins.append(Config())
configMTbins[-1].color = ROOT.kRed
configMTbins[-1].lineStyle = 1
configMTbins[-1].lineWidth = 2
configMTbins[-1].plotCfg = "HIST"
configMTbins[-1].legend = "40 < M_{T} < 80GeV"
#
configMTbins.append(Config())
configMTbins[-1].color = ROOT.kRed
configMTbins[-1].lineStyle = 2
configMTbins[-1].lineWidth = 2
configMTbins[-1].plotCfg = "HIST"
configMTbins[-1].legend = "M_{T} > 80GeV"
#####
configRegions = {}
configRegions['InvertIso_Medium_OS'] = Config()
configRegions['InvertIso_Medium_OS'].color = ROOT.kBlack
configRegions['InvertIso_Medium_OS'].lineStyle = 1
configRegions['InvertIso_Medium_OS'].lineWidth = 2
configRegions['InvertIso_Medium_OS'].plotCfg = "HIST"
configRegions['InvertIso_Medium_OS'].legend = "OS, anti-iso"
#
configRegions['InvertIso_Medium_SS'] = Config()
configRegions['InvertIso_Medium_SS'].color = ROOT.kRed
configRegions['InvertIso_Medium_SS'].lineStyle = 1
configRegions['InvertIso_Medium_SS'].lineWidth = 2
configRegions['InvertIso_Medium_SS'].plotCfg = "HIST"
configRegions['InvertIso_Medium_SS'].legend = "SS, anti-iso"
#
configRegions['Iso_Medium_OS'] = Config()
configRegions['Iso_Medium_OS'].color = ROOT.kBlack
configRegions['Iso_Medium_OS'].lineStyle = 2
configRegions['Iso_Medium_OS'].lineWidth = 2
configRegions['Iso_Medium_OS'].plotCfg = "HIST"
configRegions['Iso_Medium_OS'].legend = "OS, iso"
#
configRegions['Iso_Medium_SS'] = Config()
configRegions['Iso_Medium_SS'].color = ROOT.kRed
configRegions['Iso_Medium_SS'].lineStyle = 2
configRegions['Iso_Medium_SS'].lineWidth = 2
configRegions['Iso_Medium_SS'].plotCfg = "HIST"
configRegions['Iso_Medium_SS'].legend = "SS, iso"
