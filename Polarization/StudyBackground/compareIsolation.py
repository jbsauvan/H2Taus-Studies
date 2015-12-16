import ROOT
from copy import deepcopy
from ComparisonPlot import ComparisonPlot, Config
from HistoConfigs import configIso, configInvertIso

## Input files and histograms
histoDir = "../../../Histos/TauPolarization/Background"
version = "v_3_2015-12-16"
samples = ["W", "QCD", "TT"]
isos = [("Iso_Medium","InvertIso_Medium"), ("IsoRaw_1_5","InvertIsoRaw_1_5"), ("Iso_Medium","InvertIso_Medium_RawOnly")]
plotDir = "./plots/Isolation/"


histosIso = {}
histosInvertIso = {}
for sample in samples:
    histosIso[sample]  = ["{DIR}/{SAMPLE}/{VERSION}/polarization_background_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=sample,VERSION=version),"hPolarization_MTlt40_{ISO}_{VAR}"]
    histosInvertIso[sample] = ["{DIR}/{SAMPLE}/{VERSION}/polarization_background_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=sample,VERSION=version), "hPolarization_MTlt40_{ISO}_{VAR}"]


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
            plot.name = var+"_"+sample+"_"+iso[0]+"_"+iso[1]
            plot.plotDir = plotDir
            plot.logy = options["Log"]
            plot.legendPosition = legendPositions[var]
            #
            cfgIso = deepcopy(configIso)
            cfgIso.unitScaling = True
            cfgIso.binWidthScaling = options["VariableWidth"]
            cfgIso.xTitle = options["Title"]
            plot.addHisto(histoIso[0],histoIso[1].format(VAR=var,ISO=iso[0]), cfgIso)
            #
            cfgInvertIso = deepcopy(configInvertIso)
            cfgInvertIso.unitScaling = True
            cfgInvertIso.binWidthScaling = options["VariableWidth"]
            cfgInvertIso.xTitle = options["Title"]
            plot.addHisto(histoInvertIso[0],histoInvertIso[1].format(VAR=var,ISO=iso[1]), cfgInvertIso)
            plot.plot()
            plots.append(plot)


