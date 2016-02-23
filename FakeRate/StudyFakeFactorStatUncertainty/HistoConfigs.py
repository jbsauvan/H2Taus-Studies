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
#
configFactorStat4 = Config()
configFactorStat4.color = ROOT.kOrange+7
configFactorStat4.lineStyle = 3
configFactorStat4.lineWidth = 2
configFactorStat4.plotCfg = "HIST"
configFactorStat4.legend = ""
#
configFactorStatShifts = Config()
configFactorStatShifts.color = ROOT.kBlue
configFactorStatShifts.lineStyle = 1
configFactorStatShifts.lineWidth = 2
configFactorStatShifts.plotCfg = "HIST"
configFactorStatShifts.legend = ""
#
configsFactorStat = {}
configsFactorStat['Weight_Iso_Medium_Inclusive'] = Config()
configsFactorStat['Weight_Iso_Medium_Inclusive'].color = ROOT.kBlue
configsFactorStat['Weight_Iso_Medium_VsPt'] = Config()
configsFactorStat['Weight_Iso_Medium_VsPt'].color = ROOT.kRed
configsFactorStat['Weight_Iso_Medium_VsDecay'] = Config()
configsFactorStat['Weight_Iso_Medium_VsDecay'].color = ROOT.kMagenta
configsFactorStat['Weight_Iso_Medium_VsPtDecay'] = Config()
configsFactorStat['Weight_Iso_Medium_VsPtDecay'].color = ROOT.kOrange+7
for name,config in configsFactorStat.items():
    config.lineStyle = 1
    config.lineWidth = 2
    config.plotCfg = "HIST"
    config.legend = ""
#
configFactorUpDown = Config()
configFactorUpDown.color = ROOT.kRed
configFactorUpDown.lineStyle = 2
configFactorUpDown.lineWidth = 2
configFactorUpDown.plotCfg = "HIST"
configFactorUpDown.legend = ""


