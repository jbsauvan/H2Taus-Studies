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
#
configFactorStat2 = Config()
configFactorStat2.color = ROOT.kRed
configFactorStat2.lineStyle = 2
configFactorStat2.lineWidth = 2
configFactorStat2.plotCfg = "HIST"
configFactorStat2.legend = ""
#
configFactorStat3 = Config()
configFactorStat3.color = ROOT.kRed
configFactorStat3.lineStyle = 3
configFactorStat3.lineWidth = 2
configFactorStat3.plotCfg = "HIST"
configFactorStat3.legend = ""

configFactorUpDown = Config()
configFactorUpDown.color = ROOT.kRed
configFactorUpDown.lineStyle = 2
configFactorUpDown.lineWidth = 2
configFactorUpDown.plotCfg = "HIST"
configFactorUpDown.legend = ""


