import ROOT
import numpy as np
from array import array


def getHisto(file, name):
    histo = file.Get(name)
    if not histo:
        raise StandardError('ERROR: cannot find histo '+name)
    histo.__class__= ROOT.TH1F
    nbins = histo.GetNbinsX()
    print name
    for b in xrange(nbins+1):
        if histo.GetBinContent(b)<0:
            histo.SetBinContent(b,0)
            histo.SetBinError(b,0)
    #histo.SetAxisRange(80,200, 'X')
    return histo

def getMinimum(graph):
    xmin = graph.GetX()[0]
    xmax = graph.GetX()[graph.GetN()-1]
    min = 9999.
    xmin = 0.
    for x in np.arange(xmin,xmax, (xmax-xmin)/5000):
        if graph.Eval(x)<min:
            min = graph.Eval(x)
            xmin = x
    return xmin, min




inputFile = ROOT.TFile.Open('/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/CMSSW/CMSSW_7_4_15/src/CMGTools/H2TauTau/plotting/mt/signalRegion/StandardBackground_FromTree/v160229/datacard_mutau_standardBackground.root')
data = getHisto(inputFile, 'highMT_mt/data_obs')
w = getHisto(inputFile, 'highMT_mt/W')
tt = getHisto(inputFile, 'highMT_mt/TT')
qcd = getHisto(inputFile, 'highMT_mt/QCD')
vv = getHisto(inputFile, 'highMT_mt/VV')
zj = getHisto(inputFile, 'highMT_mt/ZJ')
zl = getHisto(inputFile, 'highMT_mt/ZL')
ztt = getHisto(inputFile, 'highMT_mt/ZTT')

sum = tt.Clone('mcs')
sum.__class__ = ROOT.TH1F
sum.Add(qcd)
sum.Add(vv)
sum.Add(zj)
sum.Add(zl)
sum.Add(ztt)


chi2s = []
cs = []
for c in np.arange(0.9,1.1,0.005):
    cs.append(c)
    wcopy = w.Clone('W_copy')
    wcopy.__class__ = ROOT.TH1F
    wcopy.Scale(c)
    wcopy.Add(sum)
    chi2 = data.Chi2Test(wcopy, 'UW CHI2/NDF')
    chi2s.append(chi2)
    wcopy.Delete()

chi2graph = ROOT.TGraph(len(chi2s), array('f',cs), array('f',chi2s))

outputfile = ROOT.TFile.Open('results/Wrescaling.root', 'RECREATE')
chi2graph.Write()


print chi2s
print getMinimum(chi2graph)




outputfile.Close()
inputFile.Close()
