import ROOT
from copy import deepcopy
from ComparisonPlot import ComparisonPlot, Config
from HistoConfigs import configIso, configInvertIso

## Input files and histograms
histoDir = "../../../Histos/TauPolarization/Background"
version = "v_1_2015-12-15"
samples = ["W", "QCD", "TT"]
isos = ["Iso_Medium", "IsoRaw_1_5"]
plotDir = "./plots/Isolation/"


histosIso = {}
histosInvertIso = {}
for sample in samples:
    histosIso[sample]  = ["{DIR}/{SAMPLE}/{VERSION}/polarization_background_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=sample,VERSION=version),"hPolarization_MTlt40_{ISO}_{VAR}"]
    histosInvertIso[sample] = ["{DIR}/{SAMPLE}/{VERSION}/polarization_background_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=sample,VERSION=version), "hPolarization_MTlt40_Invert{ISO}_{VAR}"]


## Variables and selections
variables = {
    "tau_nc_ratio":{"Title":"Neutral-Charged asymmetry", "Log":False, "VariableWidth":False},
}

legendPositions = {
    "tau_nc_ratio":[0.3, 0.2, 0.7, 0.4],
}




plots = []
for var,options in variables.items():
    for iso in isos:
        for sample in samples:
            histoIso       = histosIso[sample]
            histoInvertIso = histosInvertIso[sample]
            plot = ComparisonPlot()
            plot.name = var+"_"+sample+"_"+iso
            plot.plotDir = plotDir
            plot.logy = options["Log"]
            plot.legendPosition = legendPositions[var]
            #
            configIso = deepcopy(configIso)
            configIso.unitScaling = True
            configIso.binWidthScaling = options["VariableWidth"]
            configIso.xTitle = options["Title"]
            plot.addHisto(histoIso[0],histoIso[1].format(VAR=var,ISO=iso), configIso)
            #
            configInvertIso = deepcopy(configInvertIso)
            configInvertIso.unitScaling = True
            configInvertIso.binWidthScaling = options["VariableWidth"]
            configInvertIso.xTitle = options["Title"]
            plot.addHisto(histoInvertIso[0],histoInvertIso[1].format(VAR=var,ISO=iso), configInvertIso)
            plot.plot()
            plots.append(plot)


