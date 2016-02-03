import ROOT
import math
from array import array

inputFile = ROOT.TFile.Open('./plots/FakeFactors_ZMuMu_MT/FakeFactors_ZMuMu_MT.root')
plotDir = 'plots/HighMTCorrections/'


muon2PtCuts = [5,6,7,8,9,10,12,14,16,18,20]
muon2PtCutNames = ['Muon2PtCut_{CUT}'.format(CUT=cut) for cut in muon2PtCuts]

lowMtName  = 'MTlt40_Iso_Medium_InvertIso_Medium_nevents'
highMtName = 'MTgt70_Iso_Medium_InvertIso_Medium_nevents'


def setPlotStyle():
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetOptStat()
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetFrameLineWidth(1)
    ROOT.gStyle.SetPadBottomMargin(0.13)
    ROOT.gStyle.SetPadLeftMargin(0.13)
    ROOT.gStyle.SetPadTopMargin(0.05)
    ROOT.gStyle.SetPadRightMargin(0.03)

    ROOT.gStyle.SetLabelFont(42,"X")
    ROOT.gStyle.SetLabelFont(42,"Y")
    ROOT.gStyle.SetLabelSize(0.04,"X")
    ROOT.gStyle.SetLabelSize(0.04,"Y")
    ROOT.gStyle.SetLabelOffset(0.01,"Y")
    ROOT.gStyle.SetTickLength(0.03,"X")
    ROOT.gStyle.SetTickLength(0.03,"Y")
    ROOT.gStyle.SetLineWidth(1)
    ROOT.gStyle.SetTickLength(0.04 ,"Z")

    ROOT.gStyle.SetTitleSize(0.1)
    ROOT.gStyle.SetTitleFont(42,"X")
    ROOT.gStyle.SetTitleFont(42,"Y")
    ROOT.gStyle.SetTitleSize(0.07,"X")
    ROOT.gStyle.SetTitleSize(0.07,"Y")
    ROOT.gStyle.SetTitleOffset(0.8,"X")
    ROOT.gStyle.SetTitleOffset(0.9,"Y")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetPaintTextFormat("3.2f")
    ROOT.gROOT.ForceStyle()



def graphDivide(graph1, graph2):
    x = []
    y = []
    xe = []
    ye = []
    for p in range(0, graph1.GetN()):
        x.append(graph1.GetX()[p])
        xe.append((graph1.GetEXlow()[p]+graph1.GetEXhigh()[p])/2.)
        y1p = graph1.GetY()[p]
        y2p = graph2.GetY()[p]
        ye1p = (graph1.GetEYlow()[p]+graph1.GetEYhigh()[p])/2.
        ye2p = (graph2.GetEYlow()[p]+graph2.GetEYhigh()[p])/2.
        if y2p!=0.:
            y.append(y1p / y2p)
            ye.append(math.sqrt( (ye1p/y2p)**2 + (ye2p*y1p/y2p**2)**2 ))
        else:
            y.append(0.)
            ye.append(0.)
    print y
    graph = ROOT.TGraphErrors(len(x), array('d',x), array('d',y), array('d',xe), array('d',ye))
    graph.SetName(graph1.GetName()+"_div")
    return graph


setPlotStyle()
correctionFactors = []
correctionFactorErrors = []
for name in muon2PtCutNames:
    lowMtGraph  = inputFile.Get('{CUT}_{NAME}'.format(CUT=name,NAME=lowMtName))
    lowMtGraph.__class__ = ROOT.TGraphAsymmErrors
    highMtGraph = inputFile.Get('{CUT}_{NAME}'.format(CUT=name,NAME=highMtName))
    highMtGraph.__class__ = ROOT.TGraphAsymmErrors
    lowOverHighGraph = graphDivide(lowMtGraph, highMtGraph)
    correctionFactor = lowOverHighGraph.GetY()[0]
    correctionFactorError = lowOverHighGraph.GetEY()[0]
    correctionFactors.append(correctionFactor)
    correctionFactorErrors.append(correctionFactorError)

correctionGraph = ROOT.TGraphErrors(len(muon2PtCuts), array('f',muon2PtCuts), array('f',correctionFactors), array('f',[0.]*len(muon2PtCuts)), array('f',correctionFactorErrors))

canvas = ROOT.TCanvas('canvas', 'canvas', 800, 800)
hDummy = ROOT.TH1F('hDummy', 'hDummy', 1, 0., 21)
hDummy.SetXTitle('p_{T}(2nd muon) cut [GeV]')
hDummy.SetYTitle('Correction factor')
correctionGraph.SetMarkerStyle(20)
hDummy.Draw()
correctionGraph.Draw('lp same')
canvas.Print(plotDir+'/inclusiveHighMTCorrection_ZJet.png')

