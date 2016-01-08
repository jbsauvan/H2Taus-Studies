import ROOT
from copy import copy
from ComparisonPlot import ComparisonPlot, Config
import HistoConfigs

## Input files and histograms
histoDir = "../../../Histos/StudyFakeRate/MuTau_WJets/W/"
version = "v_1_2016-01-07"

inputFileName = "{DIR}/{VERSION}/fakerates_MuTau_WJets_W.root".format(DIR=histoDir,VERSION=version)
histoNames = "hFakeRate_{SEL}_{VAR}_vs_mt_{BIN}"

#histos = {}
#histos["InvertIso_Medium_OS_MT0"] = [inputFileName, "hFakeRate_InvertIso_Medium_OS_{VAR}_vs_mt_0"]


## Variables and selections
selectionsOSSS = ['InvertIso_Medium_OS', 'InvertIso_Medium_SS']
selectionsIso = ['Iso_Medium_OS', 'InvertIso_Medium_OS']
mtbins = [0,1,2]
variables = {
    "tau_pt":{"Title":"p_{T}^{#tau} [GeV]", "Log":True, "VariableWidth":True},
    "tau_pdgId":{"Title":"|pdg ID| #times sign-flip", "Log":False, "VariableWidth":False},
}

legendPositions = {
    "tau_pt":[0.6, 0.7, 0.95, 0.9],
    "tau_pdgId":[0.15, 0.7, 0.50, 0.9],
}

## Compare OS/SS distributions in different MT bins
plots = []
for var,options in variables.items():
    for selection in selectionsOSSS:
        plot = ComparisonPlot()
        plot.name = var+"_"+selection+'_MTbins'
        plot.plotDir = 'plots/WJets/'
        plot.logy = options["Log"]
        plot.legendPosition = legendPositions[var]
        for bin in mtbins:
            config = copy(HistoConfigs.configMTbins[bin])
            config.unitScaling = True
            config.binWidthScaling = options["VariableWidth"]
            config.xTitle = options["Title"]
            #config.legend = 'MT bin {}'.format(bin)
            plot.addHisto(inputFileName,histoNames.format(VAR=var,SEL=selection,BIN=bin), config)
        plot.plot()
        plots.append(plot)


## Compare distributions in MT bins for OS/SS regions
plots = []
for var,options in variables.items():
    for bin in mtbins:
        plot = ComparisonPlot()
        plot.name = var+"_MTBin_"+str(bin)+'_OS_SS'
        plot.plotDir = 'plots/WJets/'
        plot.logy = options["Log"]
        plot.legendPosition = legendPositions[var]
        for selection in selectionsOSSS:
            config = copy(HistoConfigs.configRegions[selection])
            config.unitScaling = True
            config.binWidthScaling = options["VariableWidth"]
            config.xTitle = options["Title"]
            #config.legend = 'MT bin {}'.format(bin)
            plot.addHisto(inputFileName,histoNames.format(VAR=var,SEL=selection,BIN=bin), config)
        plot.plot()
        plots.append(plot)

## Compare distributions in MT bins for Iso/InvertIso regions
plots = []
for var,options in variables.items():
    for bin in mtbins:
        plot = ComparisonPlot()
        plot.name = var+"_MTBin_"+str(bin)+'_Iso_InvertIso'
        plot.plotDir = 'plots/WJets/'
        plot.logy = options["Log"]
        plot.legendPosition = legendPositions[var]
        for selection in selectionsIso:
            config = copy(HistoConfigs.configRegions[selection])
            config.unitScaling = True
            config.binWidthScaling = options["VariableWidth"]
            config.xTitle = options["Title"]
            #config.legend = 'MT bin {}'.format(bin)
            plot.addHisto(inputFileName,histoNames.format(VAR=var,SEL=selection,BIN=bin), config)
        plot.plot()
        plots.append(plot)


