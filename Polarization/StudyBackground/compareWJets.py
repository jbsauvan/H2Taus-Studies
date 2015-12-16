import ROOT
from copy import copy
from ComparisonPlot import ComparisonPlot, Config
from HistoConfigs import configLowMT, configHighMT

## Input files and histograms
histoDir = "../../../Histos/TauPolarization/Background"
version = "v_3_2015-12-16"
samples = ["W"]
plotDir = "./plots/WMTCut/"

histosRef = {}
histos = {}
for sample in samples:
    histosRef[sample]  = ["{DIR}/{SAMPLE}/{VERSION}/polarization_background_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=sample,VERSION=version),"hPolarization_MTlt40_Iso_Medium_{VAR}"]
    histos[sample] = ["{DIR}/{SAMPLE}/{VERSION}/polarization_background_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=sample,VERSION=version), "hPolarization_MTgt40_Iso_Medium_{VAR}"]


## Variables and selections
variables = {
    "tau_nc_ratio":{"Title":"Neutral-Charged asymmetry", "Log":False, "VariableWidth":False},
}

legendPositions = {
    "tau_nc_ratio":[0.3, 0.2, 0.7, 0.4],
}




plots = []
for var,options in variables.items():
    for sample in histosRef.keys():
        histoRef = histosRef[sample]
        histo    = histos[sample]
        plot = ComparisonPlot()
        plot.name = var+"_"+sample+"_LowMT_vs_HighMT"
        plot.plotDir = plotDir
        plot.logy = options["Log"]
        plot.legendPosition = legendPositions[var]
        configRef = copy(configLowMT)
        configRef.unitScaling = True
        configRef.binWidthScaling = options["VariableWidth"]
        configRef.xTitle = options["Title"]
        plot.addHisto(histoRef[0],histoRef[1].format(VAR=var), configRef)
        config = copy(configHighMT)
        config.unitScaling = True
        config.binWidthScaling = options["VariableWidth"]
        config.xTitle = options["Title"]
        plot.addHisto(histo[0],histo[1].format(VAR=var), config)
        plot.plot()
        plots.append(plot)


