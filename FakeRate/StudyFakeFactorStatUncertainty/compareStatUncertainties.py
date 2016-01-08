import ROOT
from copy import copy
import numpy as np
from ComparisonPlot import ComparisonPlot, Config
from HistoConfigs import configRawStat, configFactorStat, configFactorUpDown

## Input files and histograms
histoDir = "../../../Histos/StudyFakeRate/MuTau_Stat/"
version = "v_1_2016-01-07"
samples = ["W", "TT", "QCD"]

histos = {}
for sample in samples:
    histos[sample] = ["{DIR}/{SAMPLE}/{VERSION}/fakerates_MuTau_Stat_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=sample,VERSION=version), "hFakeRate_MT40_InvertIso_Medium_mvis_vs_match5"]

systematics = []
for i in xrange(10):
    systematics.append("Weight_Iso_Medium_VsPt_Fluctuate{}".format(i))
#systematicsUpDown = []
#systematicsUpDown.append("Weight_Iso_Medium_VsPt_Up")
#systematicsUpDown.append("Weight_Iso_Medium_VsPt_Down")

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
for sample,histo in histos.items():
    plot = ComparisonPlot()
    plot.name = "statUncertainties_mvis_"+sample
    plot.logy = False
    plot.legendPosition = legendPosition
    #
    config1 = copy(configRawStat)
    config1.xTitle = "m_{T} [GeV]"
    config1.legend = "Stat. unc."
    histo1 = errorHisto(histo[0],histo[1])
    plot.addHisto(histo1, config1)
    #
    config2 = copy(configFactorStat)
    config2.xTitle = "m_{T} [GeV]"
    config2.legend = "Factor unc."
    histo2 = fakeFactorErrorHisto(histo[0],histo[1], systematics)
    plot.addHisto(histo2, config2)
    #
    config3 = copy(configFactorUpDown)
    config3.xTitle = "m_{T} [GeV]"
    config3.legend = "Up/Down unc."
    histo3 = fakeFactorUpDownErrorHisto(histo[0],histo[1], 'Weight_Iso_Medium_VsPt', 'Weight_Iso_Medium_VsPt_Up', 'Weight_Iso_Medium_VsPt_Down')
    plot.addHisto(histo3, config3)
    plot.plot()
    plots.append(plot)
