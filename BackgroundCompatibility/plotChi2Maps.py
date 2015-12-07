import ROOT
import shelve
from Data import CompatibilityData


inputdir = "../../CMSSW/CMSSW_7_4_15/src/CMGTools/H2TauTau/plotting/mt/fakeplots/"

list_weights_IsoRaw_1_5 = [
    "Weight_IsoRaw_1_5_Inclusive",
    "Weight_IsoRaw_1_5_VsNVtx",
    "Weight_IsoRaw_1_5_VsPt",
    "Weight_IsoRaw_1_5_VsEta",
    "Weight_IsoRaw_1_5_VsDecay",
    "Weight_IsoRaw_1_5_VsPdgId",
    "Weight_IsoRaw_1_5_VsPtEta",
    "Weight_IsoRaw_1_5_VsPtDecay",
    "Weight_IsoRaw_1_5_VsPtPdgId",
]
list_weights_Iso_Medium = [
    "Weight_Iso_Medium_Inclusive",
    "Weight_Iso_Medium_VsNVtx",
    "Weight_Iso_Medium_VsPt",
    "Weight_Iso_Medium_VsEta",
    "Weight_Iso_Medium_VsDecay",
    "Weight_Iso_Medium_VsPdgId",
    "Weight_Iso_Medium_VsPtEta",
    "Weight_Iso_Medium_VsPtDecay",
    "Weight_Iso_Medium_VsPtPdgId",
]

list_backgrounds = [
    ('ZJ',), 
    ('W',),
    ('TT',),
    ('T_tWch', 'TBar_tWch', 'WW', 'WZ', 'ZZ'),
    ('QCD',),
]

dict_backgrounds = {
    ('ZJ',):'Z', 
    ('W',):'W',
    ('TT',):'TT',
    ('T_tWch', 'TBar_tWch', 'WW', 'WZ', 'ZZ'):'VV',
    ('QCD',):'QCD',
}

dict_weights = {
    "Weight_IsoRaw_1_5_Inclusive":"Inclusive",
    "Weight_IsoRaw_1_5_VsNVtx":"VsNVtx",
    "Weight_IsoRaw_1_5_VsPt":"VsPt",
    "Weight_IsoRaw_1_5_VsEta":"VsEta",
    "Weight_IsoRaw_1_5_VsDecay":"VsDecay",
    "Weight_IsoRaw_1_5_VsPdgId":"VsPdgId",
    "Weight_IsoRaw_1_5_VsPtEta":"VsPtEta",
    "Weight_IsoRaw_1_5_VsPtDecay":"VsPtDecay",
    "Weight_IsoRaw_1_5_VsPtPdgId":"VsPtPdgId",
    #
    "Weight_Iso_Medium_Inclusive":"Inclusive",
    "Weight_Iso_Medium_VsNVtx":"VsNVtx",
    "Weight_Iso_Medium_VsPt":"VsPt",
    "Weight_Iso_Medium_VsEta":"VsEta",
    "Weight_Iso_Medium_VsDecay":"VsDecay",
    "Weight_Iso_Medium_VsPdgId":"VsPdgId",
    "Weight_Iso_Medium_VsPtEta":"VsPtEta",
    "Weight_Iso_Medium_VsPtDecay":"VsPtDecay",
    "Weight_Iso_Medium_VsPtPdgId":"VsPtPdgId",
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

def plotMaps(name, inputdir, list_weights, list_backgrounds):
    ## create histogram
    nweights = len(list_weights)
    nbackgrounds = len(list_backgrounds)

    pvaluemap = ROOT.TH2F("pvalue_vs_background_and_weight_"+name, "", nweights, 0., nweights, nbackgrounds, 0., nbackgrounds)
    chi2map = ROOT.TH2F("chi2_vs_background_and_weight_"+name, "", nweights, 0., nweights, nbackgrounds, 0., nbackgrounds)
    chi2normmap = ROOT.TH2F("chi2norm_vs_background_and_weight_"+name, "", nweights, 0., nweights, nbackgrounds, 0., nbackgrounds)
    for b in xrange(1, chi2map.GetNbinsX()+1):
        pvaluemap.GetXaxis().SetBinLabel(b, dict_weights[list_weights[b-1]])
        chi2map.GetXaxis().SetBinLabel(b, dict_weights[list_weights[b-1]])
        chi2normmap.GetXaxis().SetBinLabel(b, dict_weights[list_weights[b-1]])
    for b in xrange(1, chi2map.GetNbinsY()+1):
        pvaluemap.GetYaxis().SetBinLabel(b, dict_backgrounds[list_backgrounds[b-1]])
        chi2map.GetYaxis().SetBinLabel(b, dict_backgrounds[list_backgrounds[b-1]])
        chi2normmap.GetYaxis().SetBinLabel(b, dict_backgrounds[list_backgrounds[b-1]])


    data = shelve.open(inputdir+"/background_compatibility.db",'r')
    for key in data:
        dat = CompatibilityData()
        dat.fillFromDict(data[key])
        backgrounds = tuple(dat.backgrounds)
        weight = dat.weight_name
        if not backgrounds in list_backgrounds: continue
        if not weight in list_weights: continue
        binx = chi2map.GetXaxis().FindBin(dict_weights[weight])
        biny = chi2map.GetYaxis().FindBin(dict_backgrounds[backgrounds])
        print dat.chi2[0]
        pvaluemap.SetBinContent(binx,biny, dat.chi2[0])
        chi2map.SetBinContent(binx,biny, dat.chi2[1])
        chi2normmap.SetBinContent(binx,biny, dat.chi2[2])


    canvas = []

    setPlotStyle()

    pvaluemap.SetContour(99)
    canvas.append(ROOT.TCanvas("canvas_pvalue_{}".format(name), "canvas", 700, 700))
    canvas[-1].SetLogz()
    pvaluemap.SetAxisRange(1.e-30, 1., "Z")
    pvaluemap.Draw("col text")
    canvas[-1].Print("plots/pvaluemap_{}.png".format(name))
    canvas[-1].Print("plots/pvaluemap_{}.eps".format(name))
    canvas[-1].Print("plots/pvaluemap_{}.pdf".format(name))

    chi2map.SetContour(99)
    canvas.append(ROOT.TCanvas("canvas_chi2_{}".format(name), "canvas", 700, 700))
    canvas[-1].SetLogz()
    chi2map.Draw("col text")
    canvas[-1].Print("plots/chi2map_{}.png".format(name))
    canvas[-1].Print("plots/chi2map_{}.eps".format(name))
    canvas[-1].Print("plots/chi2map_{}.pdf".format(name))

    chi2normmap.SetContour(99)
    canvas.append(ROOT.TCanvas("canvas_chi2norm_{}".format(name), "canvas", 700, 700))
    canvas[-1].SetLogz()
    chi2normmap.Draw("col text")
    canvas[-1].Print("plots/chi2normmap_{}.png".format(name))
    canvas[-1].Print("plots/chi2normmap_{}.eps".format(name))
    canvas[-1].Print("plots/chi2normmap_{}.pdf".format(name))

    #outfile = ROOT.TFile("test.root", "RECREATE")
    #for c in canvas:
        #c.Write()
    #outfile.Close()
    data.close()

setPlotStyle()
plotMaps("IsoRaw_1_5",inputdir, list_weights_IsoRaw_1_5, list_backgrounds)
plotMaps("Iso_Medium",inputdir, list_weights_Iso_Medium, list_backgrounds)

