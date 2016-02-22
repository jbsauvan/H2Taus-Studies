import ROOT
from copy import copy
from ComparisonPlot import ComparisonPlot, Config
import HistoConfigs 

## Input files and histograms
histoDir = "../../../Histos/StudyFakeRate/MuTau/AllFakeFactors/"
version = "v_6_2016-02-22"

fakefactors= {
    'HighMT':'W',
}

histos = {
    'MT40':{
        'File':'{DIR}/{SAMPLE}/{VERSION}/fakerates_MuTau_{SAMPLE}.root',
        'HistoTrue':'hFakeRate_MT40_Iso_Medium_{VAR}',
        'HistoEst':'Weight_{FACTOR}_Iso_Medium_VsPtDecay/hFakeRate_MT40_InvertIso_Medium_{VAR}',
    },
    'AllMT':{
        'File':'{DIR}/{SAMPLE}/{VERSION}/fakerates_MuTau_{SAMPLE}.root',
        'HistoTrue':'hFakeRate_Iso_Medium_{VAR}',
        'HistoEst':'Weight_{FACTOR}_Iso_Medium_VsPtDecay/hFakeRate_InvertIso_Medium_{VAR}',
    },
}

## Variables and selections
variables = {
    #"mvis_stdbins":{"Title":"m_{vis}", "Log":False, "VariableWidth":True},
    "njets":{"Title":"N_{jets}", "Log":True, "VariableWidth":False},
    "njets20":{"Title":"N_{jets}", "Log":True, "VariableWidth":False},
}

legendPositions = {
    "mvis_stdbins":[0.6, 0.7, 0.95, 0.9],
    "njets":[0.6, 0.7, 0.95, 0.9],
    "njets20":[0.6, 0.7, 0.95, 0.9],
}




plots = []
for var,options in variables.items():
    for fakefactor,sample in fakefactors.items():
        for name,histo in histos.items():
            filename = histo['File'].format(DIR=histoDir,SAMPLE=sample,VERSION=version)
            histoTrue = histo['HistoTrue'].format(VAR=var)
            histoEst = histo['HistoEst'].format(FACTOR=fakefactor,VAR=var)
            #
            plot = ComparisonPlot()
            plot.plotDir = 'results/'
            plot.name = var+"_"+name+'_'+fakefactor+"_"+sample
            plot.xRange  = [0.,5.9999]
            plot.yRatioRange = [0.5,4.5]
            plot.logy = options["Log"]
            plot.legendPosition = legendPositions[var]
            configTrue = copy(HistoConfigs.configTrue)
            #configTrue.unitScaling = True
            configTrue.binWidthScaling = options["VariableWidth"]
            configTrue.xTitle = options["Title"]
            configTrue.legend = 'True'
            plot.addHisto(filename,histoTrue, configTrue)
            configEst = copy(HistoConfigs.configEst)
            #configEst.unitScaling = True
            configEst.binWidthScaling = options["VariableWidth"]
            configEst.xTitle = options["Title"]
            configEst.legend = 'Est.'
            plot.addHisto(filename,histoEst, configEst)
            plot.plot()
            plot.plot_ratio()
            plots.append(plot)


