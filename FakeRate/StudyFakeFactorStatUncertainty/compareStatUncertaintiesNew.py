import ROOT
from copy import copy
import numpy as np
from ComparisonPlot import ComparisonPlot, Config
from HistoConfigs import *
import SysCalculator

## Input files and histograms
histoDir = "../../../Histos/StudyFakeRate/MuTau/FakeFactorUncertaintiesFromToys/"
version = "v_1_2016-02-23"
histoDir2 = "../../../Histos/StudyFakeRate/MuTau/FakeFactorUncertainties/"
version2 = "v_5_2016-02-19"
samples = {
    'Data':['Data_Run15D_05Oct','Data_Run15D_v4']
}

histos1 = {}
histos2 = {}
for name,sample in samples.items():
    histoList = []
    histos1[name] = []
    histos2[name] = []
    for s in sample:
        histos1[name].append(["{DIR}/{SAMPLE}/{VERSION}/fakerates_MuTau_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=s,VERSION=version), "hFakeRate_MT40_InvertIso_Medium_mvis_stdbins"])
        histos2[name].append(["{DIR}/{SAMPLE}/{VERSION}/fakerates_MuTau_{SAMPLE}.root".format(DIR=histoDir2,SAMPLE=s,VERSION=version2), "hFakeRate_MT40_InvertIso_Medium_mvis_stdbins"])

systematics = {
    'Weight_Combined_Iso_Medium_VsPtDecay':[],
}
systematics2 = {
    'Weight_Combined_Iso_Medium_VsPtDecay':[],
}
for name,sys in systematics.items():
    for i in xrange(200):
        sys.append("{NAME}_Fluctuate{I}".format(NAME=name,I=i))


systematicsLegends = {}
systematicsLegends['Weight_Combined_Iso_Medium_VsPtDecay'] = 'p_{T} + decay'

legendPosition = [0.2, 0.7, 0.45, 0.9]

def loadHisto(fileName, histoName):
    file = ROOT.TFile.Open(fileName)
    if not file: raise StandardError("Cannot open file "+fileName)
    histo = file.Get(histoName)
    if not histo: raise StandardError("Cannot load histogram "+histoName+" from file "+fileName)
    histo.__class__ = ROOT.TH1F
    histo.SetDirectory(0)
    file.Close()
    return histo


def sumHistos(fileNames, histoNames):
    histoSum = None
    for fileName,histoName in zip(fileNames,histoNames):
        histo = loadHisto(fileName, histoName)
        if not histoSum: 
            histoSum = histo.Clone(histo.GetName()+'_sum')
            histoSum.__class__ = ROOT.TH1F
            histoSum.SetDirectory(0)
        else: histoSum.Add(histo)
    return histoSum



def errorHisto(fileNames, histoNames):
    histo = sumHistos(fileNames, histoNames)
    errors = histo.Clone(histo.GetName()+"_errors")
    nbins = errors.GetNbinsX()
    for b in xrange(1,nbins+1):
        error = histo.GetBinError(b)
        content = histo.GetBinContent(b)
        errors.SetBinContent(b, error/content if content>0 else 0)
        errors.SetBinError(b,0.)
    histo.Delete()
    return errors


def fakeFactorErrorHisto(fileNames, histoNames, sysNames):
    variations = []
    histo = sumHistos(fileNames, histoNames)
    errors = histo.Clone(histo.GetName()+"_fferrors")
    errors.SetDirectory(0)
    histo.Delete()
    nbins = errors.GetNbinsX()
    for b in xrange(nbins):
        variations.append([])
    for sys in sysNames:
        histo = sumHistos(fileNames, [sys+'/'+histoName for histoName in histoNames])
        for b in xrange(1,nbins+1):
            variations[b-1].append(histo.GetBinContent(b))
        histo.Delete()
    for b in xrange(1,nbins+1):
        mean = np.mean(variations[b-1])
        sigma = np.std(variations[b-1])
        errors.SetBinContent(b, sigma/mean if mean>0 else 0)
        errors.SetBinError(b,0)
    return errors

def fakeFactorSysErrorHisto(fileNames, histoNames, nomName, sysNames):
    variations = []
    histo = sumHistos(fileNames, [nomName+'/'+histoName for histoName in histoNames])
    histo_sys = []
    for sys in sysNames:
        histo_sys.append(sumHistos(fileNames, [sys+'/'+histoName for histoName in histoNames]))
    sysCalc = SysCalculator.DefaultSysCalculator()
    histoDown,histoUp = sysCalc.getSystematics(histo, histo_sys)
    #for b in xrange(1, histo.GetNbinsX()+1):
        #print histo.GetBinContent(b), histoUp.GetBinContent(b)
    histoUp.Add(histo, -1.)
    histoUp.Divide(histo)
    #for b in xrange(1, histo.GetNbinsX()+1):
        #print histoUp.GetBinContent(b)
    return histoUp

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
    for sample,histo in histos1.items():
        plot = ComparisonPlot()
        plot.name = "statUncertainties_mvis_"+sample+'_'+name
        plot.logy = False
        plot.legendPosition = legendPosition
        #
        config1 = copy(configRawStat)
        config1.xTitle = "m_{vis} [GeV]"
        config1.yTitle = 'Relative uncertainty'
        config1.legend = "Stat. unc."
        histo1 = errorHisto([h[0] for h in histo] ,[name+'/'+h[1] for h in histo])
        plot.addHisto(histo1, config1)
        #
        #config2 = copy(configFactorStat4)
        #config2.xTitle = "m_{vis} [GeV]"
        #config2.legend = "Factor unc. 10"
        #config2.yTitle = 'Relative uncertainty'
        #histo2 = fakeFactorErrorHisto([h[0] for h in histo],[h[1] for h in histo] sys[10:20])
        #plot.addHisto(histo2, config2)
        #
        config3 = copy(configFactorStat3)
        config3.xTitle = "m_{vis} [GeV]"
        config3.legend = "Factor unc. 50"
        config3.yTitle = 'Relative uncertainty'
        histo3 = fakeFactorErrorHisto([h[0] for h in histo],[h[1] for h in histo], sys[0:50])
        plot.addHisto(histo3, config3)
        #
        config4 = copy(configFactorStat2)
        config4.xTitle = "m_{vis} [GeV]"
        config4.legend = "Factor unc. 100"
        config4.yTitle = 'Relative uncertainty'
        histo4 = fakeFactorErrorHisto([h[0] for h in histo],[h[1] for h in histo], sys[0:100])
        plot.addHisto(histo4, config4)
        #
        config5 = copy(configFactorStat)
        config5.xTitle = "m_{vis} [GeV]"
        config5.legend = "Factor unc. 200"
        config5.yTitle = 'Relative uncertainty'
        histo5 = fakeFactorErrorHisto([h[0] for h in histo],[h[1] for h in histo], sys[0:200])
        plot.addHisto(histo5, config5)
        # Error from individual shifts
        histo2 = histos2[sample]
        shifts = []
        for h in histo2:
            f = ROOT.TFile.Open(h[0])
            keys = f.GetListOfKeys()
            for key in keys:
                if key.IsFolder() and 'ShiftStat' in key.GetName():
                    #print key.GetName()
                    if not key.GetName() in shifts: shifts.append(key.GetName())
        config6 = copy(configFactorStatShifts)
        config6.xTitle = "m_{vis} [GeV]"
        config6.legend = "Individual shifts"
        config6.yTitle = 'Relative uncertainty'
        histo6 = fakeFactorSysErrorHisto([h[0] for h in histo2],[h[1] for h in histo2], name, shifts)
        plot.addHisto(histo6, config6)
        #
        plot.plot()
        plots.append(plot)

