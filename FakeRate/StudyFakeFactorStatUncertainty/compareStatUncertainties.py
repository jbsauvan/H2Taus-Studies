import ROOT
from copy import copy
import numpy as np
from ComparisonPlot import ComparisonPlot, Config
from HistoConfigs import *

## Input files and histograms
histoDir = "../../../Histos/StudyFakeRate/MuTau_Stat/"
version = "v_4_2016-01-10"
samples = ["W", "TT", "QCD"]

histos = {}
for sample in samples:
    histos[sample] = ["{DIR}/{SAMPLE}/{VERSION}/fakerates_MuTau_Stat_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=sample,VERSION=version), "hFakeRate_MT40_InvertIso_Medium_mvis_vs_match5"]

systematics = {
    'Weight_Iso_Medium_Inclusive':[],
    'Weight_Iso_Medium_VsPt':[],
    'Weight_Iso_Medium_VsDecay':[],
    'Weight_Iso_Medium_VsPtDecay':[],
}
for name,sys in systematics.items():
    for i in xrange(200):
        sys.append("{NAME}_Fluctuate{I}".format(NAME=name,I=i))
#systematicsUpDown = []
#systematicsUpDown.append("Weight_Iso_Medium_VsPt_Up")
#systematicsUpDown.append("Weight_Iso_Medium_VsPt_Down")

systematicsLegends = {}
systematicsLegends['Weight_Iso_Medium_Inclusive'] = 'inclusive'
systematicsLegends['Weight_Iso_Medium_VsPt'] = 'p_{T}'
systematicsLegends['Weight_Iso_Medium_VsDecay'] = 'decay'
systematicsLegends['Weight_Iso_Medium_VsPtDecay'] = 'p_{T} + decay'

legendPosition = [0.2, 0.7, 0.45, 0.9]


def errorHisto(fileName, histoName):
    file = ROOT.TFile.Open(fileName)
    if not file: raise StandardError("Cannot open file "+fileName)
    histo = file.Get(histoName)
    if not histo: raise StandardError("Cannot load histogram "+histoName+" from file "+fileName)
    histo.__class__ = ROOT.TH1F
    histo.SetDirectory(0)
    file.Close()
    errors = histo.Clone(histo.GetName()+"_errors")
    nbins = errors.GetNbinsX()
    for b in xrange(1,nbins+1):
        error = histo.GetBinError(b)
        content = histo.GetBinContent(b)
        errors.SetBinContent(b, error/content if content>0 else 0)
        errors.SetBinError(b,0.)
    histo.Delete()
    return errors


def fakeFactorErrorHisto(fileName, histoName, sysNames):
    variations = []
    file = ROOT.TFile.Open(fileName)
    if not file: raise StandardError("Cannot open file "+fileName)
    histo = file.Get(histoName)
    if not histo: raise StandardError("Cannot load histogram "+histoName+" from file "+fileName)
    histo.__class__ = ROOT.TH1F
    histo.SetDirectory(0)
    errors = histo.Clone(histo.GetName()+"_fferrors")
    errors.SetDirectory(0)
    histo.Delete()
    nbins = errors.GetNbinsX()
    for b in xrange(nbins):
        variations.append([])
    for sys in sysNames:
        histo = file.Get(sys+"/"+histoName)
        if not histo: raise StandardError("Cannot load histogram "+sys+"/"+histoName+" from file "+fileName)
        histo.__class__ = ROOT.TH1F
        histo.SetDirectory(0)
        for b in xrange(1,nbins+1):
            variations[b-1].append(histo.GetBinContent(b))
        histo.Delete()
    for b in xrange(1,nbins+1):
        mean = np.mean(variations[b-1])
        sigma = np.std(variations[b-1])
        errors.SetBinContent(b, sigma/mean if mean>0 else 0)
        errors.SetBinError(b,0)
    file.Close()
    return errors

def fakeFactorUpDownErrorHisto(fileName, histoName, sysNom, sysUp, sysDown):
    variations = []
    file = ROOT.TFile.Open(fileName)
    if not file: raise StandardError("Cannot open file "+fileName)
    #
    histoNom = file.Get(sysNom+'/'+histoName)
    if not histoNom: raise StandardError("Cannot load histogram "+sysNom+'/'+histoName+" from file "+fileName)
    histoNom.__class__ = ROOT.TH1F
    histoNom.SetDirectory(0)
    #
    histoUp = file.Get(sysUp+'/'+histoName)
    if not histoUp: raise StandardError("Cannot load histogram "+sysUp+'/'+histoName+" from file "+fileName)
    histoUp.__class__ = ROOT.TH1F
    histoUp.SetDirectory(0)
    #
    histoDown = file.Get(sysDown+'/'+histoName)
    if not histoDown: raise StandardError("Cannot load histogram "+sysDown+'/'+histoName+" from file "+fileName)
    histoDown.__class__ = ROOT.TH1F
    histoDown.SetDirectory(0)
    #
    errors = histoNom.Clone(histoNom.GetName()+"_fupdownerrors")
    errors.SetDirectory(0)
    nbins = errors.GetNbinsX()
    for b in xrange(1,nbins+1):
        nom  = histoNom.GetBinContent(b)
        up   = histoUp.GetBinContent(b)
        down = histoDown.GetBinContent(b)
        error = (abs(up-nom)+abs(down-nom))/2. ## average of up and down absolute shifts
        errors.SetBinContent(b, error/nom if nom>0 else 0)
        errors.SetBinError(b,0)
    file.Close()
    return errors
    



plots = []
## Compare uncertainties with several numbers of tries
for name,sys in systematics.items():
    for sample,histo in histos.items():
        plot = ComparisonPlot()
        plot.name = "statUncertainties_mvis_"+sample+'_'+name
        plot.logy = False
        plot.legendPosition = legendPosition
        #
        config1 = copy(configRawStat)
        config1.xTitle = "m_{vis} [GeV]"
        config1.yTitle = 'Relative uncertainty'
        config1.legend = "Stat. unc."
        histo1 = errorHisto(histo[0],name+'/'+histo[1])
        plot.addHisto(histo1, config1)
        #
        config2 = copy(configFactorStat4)
        config2.xTitle = "m_{vis} [GeV]"
        config2.legend = "Factor unc. 10"
        config2.yTitle = 'Relative uncertainty'
        histo2 = fakeFactorErrorHisto(histo[0],histo[1], sys[10:20])
        plot.addHisto(histo2, config2)
        #
        config3 = copy(configFactorStat3)
        config3.xTitle = "m_{vis} [GeV]"
        config3.legend = "Factor unc. 50"
        config3.yTitle = 'Relative uncertainty'
        histo3 = fakeFactorErrorHisto(histo[0],histo[1], sys[0:50])
        plot.addHisto(histo3, config3)
        #
        config4 = copy(configFactorStat2)
        config4.xTitle = "m_{vis} [GeV]"
        config4.legend = "Factor unc. 100"
        config4.yTitle = 'Relative uncertainty'
        histo4 = fakeFactorErrorHisto(histo[0],histo[1], sys[0:100])
        plot.addHisto(histo4, config4)
        #
        config5 = copy(configFactorStat)
        config5.xTitle = "m_{vis} [GeV]"
        config5.legend = "Factor unc. 200"
        config5.yTitle = 'Relative uncertainty'
        histo5 = fakeFactorErrorHisto(histo[0],histo[1], sys[0:200])
        plot.addHisto(histo5, config5)
        #
        plot.plot()
        plots.append(plot)
#
## Compare uncertainties for different fake factors
for sample,histo in histos.items():
    plot = ComparisonPlot()
    plot.name = "statUncertainties_mvis_"+sample
    plot.logy = False
    plot.legendPosition = [0.2, 0.65, 0.55, 0.9]
    #
    configs = {}
    histos = {}
    for name,sys in systematics.items():
        configs[name] = copy(configsFactorStat[name])
        configs[name].xTitle = "m_{vis} [GeV]"
        configs[name].yTitle = 'Relative uncertainty'
        configs[name].legend = systematicsLegends[name]
        histos[name] = fakeFactorErrorHisto(histo[0],histo[1], sys[0:200])
        plot.addHisto(histos[name], configs[name])
        #
        plot.plot()
        plots.append(plot)
