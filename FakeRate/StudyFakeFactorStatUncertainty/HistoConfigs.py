import ROOT
from ComparisonPlot import Config

configRawStat = Config()
configRawStat.color = ROOT.kBlack
configRawStat.lineStyle = 1
configRawStat.lineWidth = 2
configRawStat.plotCfg = "HIST"
configRawStat.legend = ""


configFactorStat = Config()
configFactorStat.color = ROOT.kRed
configFactorStat.lineStyle = 1
configFactorStat.lineWidth = 2
configFactorStat.plotCfg = "HIST"
configFactorStat.legend = ""

configFactorUpDown = Config()
configFactorUpDown.color = ROOT.kRed
configFactorUpDown.lineStyle = 2
configFactorUpDown.lineWidth = 2
configFactorUpDown.plotCfg = "HIST"
configFactorUpDown.legend = ""


