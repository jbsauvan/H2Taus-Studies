import ROOT
from copy import copy
from ComparisonPlot import ComparisonPlot, Config
from HistoConfigs import configZMuMu, configMuTau

## Input files and histograms
histoDir = "../../Histos/StudyFakeRate/"
ZMuMuVersion = "v_4_2015-11-25"
MuTauVersion = "v_6_2015-11-30"
MuTauSamples = ["W", "TT", "QCD", "ZJ"]

histosRef = {}
histosRef["ZMuMuX"] = ["{DIR}/ZMuMu/{VERSION}/fakerates_ZMuMu.root".format(DIR=histoDir,VERSION=ZMuMuVersion),"hFakeRate_InvertIso_{VAR}"]
histos = {}
for sample in MuTauSamples:
    histos[sample] = ["{DIR}/MuTau/{SAMPLE}/{VERSION}/fakerates_MuTau_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=sample,VERSION=MuTauVersion), "hFakeRate_InvertIso_{VAR}_vs_match5"]


## Variables and selections
variables = {
    "tau_pt":{"Title":"p_{T}^{#tau} [GeV]", "Log":True, "VariableWidth":True},
    "tau_eta":{"Title":"#eta^{#tau}", "Log":False, "VariableWidth":False},
    "tau_decayMode":{"Title":"tau decay mode", "Log":False, "VariableWidth":False},
    "tau_pdgId":{"Title":"pdg ID #times sign-flip", "Log":False, "VariableWidth":False},
}

legendPositions = {
    "tau_pt":[0.7, 0.7, 0.9, 0.9],
    "tau_eta":[0.75, 0.8, 0.95, 0.93],
    "tau_decayMode":[0.2, 0.7, 0.4, 0.9],
    "tau_pdgId":[0.2, 0.7, 0.4, 0.9],
}




plots = []
for var,options in variables.items():
    for nameRef,histoRef in histosRef.items():
        for name,histo in histos.items():
            plot = ComparisonPlot()
            plot.name = var+"_"+nameRef+"_"+name
            plot.logy = options["Log"]
            plot.legendPosition = legendPositions[var]
            configRef = copy(configZMuMu)
            configRef.unitScaling = True
            configRef.binWidthScaling = options["VariableWidth"]
            configRef.xTitle = options["Title"]
            plot.addHisto(histoRef[0],histoRef[1].format(VAR=var), configRef)
            config = copy(configMuTau)
            config.unitScaling = True
            config.binWidthScaling = options["VariableWidth"]
            config.xTitle = options["Title"]
            config.legend = name+" "+config.legend
            plot.addHisto(histo[0],histo[1].format(VAR=var), config)
            plot.plot()
            plots.append(plot)


