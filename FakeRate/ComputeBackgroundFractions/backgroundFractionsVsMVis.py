import ROOT
from EfficiencyPlots import EfficiencyPlot, PlotInfo


#inputFile = ROOT.TFile.Open('../../../CMSSW/CMSSW_7_4_15/src/CMGTools/H2TauTau/plotting/mt/datacard_mutau_qcdFromSS.root')
#directory = 'lowMT_mvis'
inputFile = ROOT.TFile.Open('../../../CMSSW/CMSSW_7_4_15/src/CMGTools/H2TauTau/plotting/mt/signalRegion/StandardBackgroundFakeOnly/v160209/datacard_mutau_standardBackgroundFakeOnly.root')
directory = 'MT40_Iso_Medium_mvis_stdbins'

backgrounds = ['VV', 'TT', 'QCD', 'W', 'ZJ']

## Retrieve histograms
histos = {}
histo_total = None
for background in backgrounds:
    histos[background] = inputFile.Get('{DIR}/{HISTO}'.format(DIR=directory,HISTO=background))
    histos[background].__class__ = ROOT.TH1F
    if not histo_total: histo_total = histos[background].Clone('{DIR}_sum'.format(DIR=directory))
    else: histo_total.Add(histos[background])

plots = []
for background,histo in histos.items():
    plot = EfficiencyPlot()
    plot.name = "backgroundFraction_{DIR}_{BACK}".format(DIR=directory,BACK=background)
    plot.plotDir = "results/"
    plot.publicationDir = ""
    plot.efficiency(histo, histo_total, "cp", PlotInfo())
    plot.plot(0, 1)
    plots.append(plot)

outputFile = ROOT.TFile.Open('results/backgroundFraction_{DIR}.root'.format(DIR=directory), 'RECREATE')
for plot in plots:
    for graph in plot.efficiencyGraphs:
        graph.SetName('g_'+plot.name)
        graph.Write()
    for histo in plot.efficiencyHistos:
        histo.SetName('h_'+plot.name)
        histo.Write()

outputFile.Close()
inputFile.Close()
