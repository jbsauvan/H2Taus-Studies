import ROOT
import shelve
from Data import CompatibilityData


inputdir = "../../CMSSW/CMSSW_7_4_15/src/CMGTools/H2TauTau/plotting/mt/fakeplots/"

list_weights = [
    "Weight_Inclusive",
    "Weight_VsNVtx",
    "Weight_VsPt",
    "Weight_VsEta",
    "Weight_VsDecay",
    "Weight_VsPdgId",
    "Weight_VsPtEta",
    "Weight_VsPtDecay",
    "Weight_VsPtPdgId",
]

list_backgrounds = [
    ('ZJ',), 
    ('W',),
    ('TT',),
    ('T_tWch', 'TBar_tWch', 'WW', 'WZ', 'ZZ'),
    ('QCD',),
]

dict_names = {
    ('ZJ',):'Z', 
    ('W',):'W',
    ('TT',):'TT',
    ('T_tWch', 'TBar_tWch', 'WW', 'WZ', 'ZZ'):'VV',
    ('QCD',):'QCD',
}


def setPlotStyle():
    ROOT.gROOT.SetStyle("Plain");
    ROOT.gStyle.SetOptStat(0);
    ROOT.gStyle.SetOptFit(0);
    ROOT.gStyle.SetOptTitle(0);
    ROOT.gStyle.SetFrameLineWidth(1);
    ROOT.gStyle.SetPadBottomMargin(0.12);
    ROOT.gStyle.SetPadLeftMargin(0.12);
    ROOT.gStyle.SetPadTopMargin(0.12);
    ROOT.gStyle.SetPadRightMargin(0.12);

    ROOT.gStyle.SetLabelFont(42,"X");
    ROOT.gStyle.SetLabelFont(42,"Y");
    ROOT.gStyle.SetLabelSize(0.05,"X");
    ROOT.gStyle.SetLabelSize(0.05,"Y");
    ROOT.gStyle.SetLabelOffset(0.01,"Y");
    ROOT.gStyle.SetTickLength(0.04,"X");
    ROOT.gStyle.SetTickLength(0.04,"Y");
    ROOT.gStyle.SetLineWidth(1);
    ROOT.gStyle.SetTickLength(0.04 ,"Z");

    ROOT.gStyle.SetTitleSize(0.1);
    ROOT.gStyle.SetTitleFont(42,"X");
    ROOT.gStyle.SetTitleFont(42,"Y");
    ROOT.gStyle.SetTitleSize(0.05,"X");
    ROOT.gStyle.SetTitleSize(0.05,"Y");
    ROOT.gStyle.SetTitleOffset(1.1,"X");
    ROOT.gStyle.SetTitleOffset(1.3,"Y");
    ROOT.gStyle.SetPalette(1);
    ROOT.gStyle.SetPaintTextFormat("3.2f")
    ROOT.gROOT.ForceStyle();


## create histogram
nweights = len(list_weights)
nbackgrounds = len(list_backgrounds)

chi2map = ROOT.TH2F("chi2_vs_background_and_weight", "", nweights, 0., nweights, nbackgrounds, 0., nbackgrounds)
chi2normmap = ROOT.TH2F("chi2norm_vs_background_and_weight", "", nweights, 0., nweights, nbackgrounds, 0., nbackgrounds)
for b in xrange(1, chi2map.GetNbinsX()+1):
    chi2map.GetXaxis().SetBinLabel(b, list_weights[b-1])
    chi2normmap.GetXaxis().SetBinLabel(b, list_weights[b-1])
for b in xrange(1, chi2map.GetNbinsY()+1):
    chi2map.GetYaxis().SetBinLabel(b, dict_names[list_backgrounds[b-1]])
    chi2normmap.GetYaxis().SetBinLabel(b, dict_names[list_backgrounds[b-1]])


data = shelve.open(inputdir+"/background_compatibility.db",'r')
for key in data:
    dat = CompatibilityData()
    dat.fillFromDict(data[key])
    backgrounds = tuple(dat.backgrounds)
    weight = dat.weight_name
    if not backgrounds in list_backgrounds: continue
    if not weight in list_weights: continue
    binx = chi2map.GetXaxis().FindBin(weight)
    biny = chi2map.GetYaxis().FindBin(dict_names[backgrounds])
    chi2map.SetBinContent(binx,biny, dat.chi2[0])
    chi2normmap.SetBinContent(binx,biny, dat.chi2[1])


canvas = []

setPlotStyle()
chi2map.SetContour(99)
canvas.append(ROOT.TCanvas("canvas_chi2", "canvas", 700, 700))
canvas[-1].SetLogz()
chi2map.Draw("col text")
canvas[-1].Print("plots/chi2map.png")
canvas[-1].Print("plots/chi2map.eps")
canvas[-1].Print("plots/chi2map.pdf")

chi2normmap.SetContour(99)
canvas.append(ROOT.TCanvas("canvas_chi2norm", "canvas", 700, 700))
canvas[-1].SetLogz()
chi2normmap.Draw("col text")
canvas[-1].Print("plots/chi2normmap.png")
canvas[-1].Print("plots/chi2normmap.eps")
canvas[-1].Print("plots/chi2normmap.pdf")

outfile = ROOT.TFile("test.root", "RECREATE")
for c in canvas:
    c.Write()
outfile.Close()
data.close()


