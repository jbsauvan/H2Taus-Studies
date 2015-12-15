import ROOT
from copy import copy
from ComparisonPlot import ComparisonPlot, Config
from HistoConfigs import configBackgrounds

## Input files and histograms
histoDir = "../../../Histos/TauPolarization/Background"
version = "v_1_2015-12-15"
samples = ["W", "TT"]
#samples = ["W", "QCD", "TT"]
plotDir = "./plots/Backgrounds/"

histos = {}
for sample in samples:
    histos[sample] = ["{DIR}/{SAMPLE}/{VERSION}/polarization_background_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=sample,VERSION=version), "hPolarization_MTlt40_Iso_Medium_{VAR}"]


## Variables and selections
variables = {
    "tau_nc_ratio":{"Title":"Neutral-Charged asymmetry", "Log":False, "VariableWidth":False},
}

legendPositions = {
    "tau_nc_ratio":[0.3, 0.2, 0.7, 0.4],
}




plots = []
for var,options in variables.items():
    plot = ComparisonPlot()
    plot.name = var+"_backgrounds"
    plot.plotDir = plotDir
    plot.logy = options["Log"]
    plot.legendPosition = legendPositions[var]
    for sample,histo in histos.items():
        config = copy(configBackgrounds[sample])
        config.unitScaling = True
        config.binWidthScaling = options["VariableWidth"]
        config.xTitle = options["Title"]
        plot.addHisto(histo[0],histo[1].format(VAR=var), config)
    plot.plot()
    plots.append(plot)


