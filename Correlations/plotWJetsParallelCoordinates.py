import ROOT

ROOT.gROOT.SetStyle("Plain");
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptFit(0);
ROOT.gStyle.SetOptTitle(0);
ROOT.gStyle.SetFrameLineWidth(1);
ROOT.gStyle.SetPadBottomMargin(0.12);
ROOT.gStyle.SetPadLeftMargin(0.12);
ROOT.gStyle.SetPadTopMargin(0.03);
ROOT.gStyle.SetPadRightMargin(0.12);

ROOT.gStyle.SetLabelFont(42,"X");
ROOT.gStyle.SetLabelFont(42,"Y");
ROOT.gStyle.SetLabelSize(0.03,"X");
ROOT.gStyle.SetLabelSize(0.03,"Y");
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
ROOT.gStyle.SetTitleOffset(1.1,"Y");
ROOT.gStyle.SetPalette(1);
ROOT.gStyle.SetPaintTextFormat("3.2f")
ROOT.gROOT.ForceStyle();

inputFile = ROOT.TFile.Open('/afs/cern.ch/work/s/steggema/public/mt/18112015/WJetsToLNu_LO/H2TauTauTreeProducerTauMu/tree.root')
tree = inputFile.Get('tree')

cuts = ''
cuts += 'l1_muonid_medium>0.5 && l1_pt>19 && l1_reliso05<0.1'
cuts += ' && l2_againstMuon3>1.5 && l2_againstElectronMVA5>0.5 && l2_decayModeFinding'
cuts += ' && veto_dilepton<0.5 && veto_thirdlepton<0.5 && veto_otherlepton<0.5'
cuts += ' && l2_decayModeFinding'
cuts += ' && l2_pt>20'
cuts += ' && l2_gen_match==6'
#cuts += ' && l2_byCombinedIsolationDeltaBetaCorr3Hits>=2'

visualCuts = ' mt<100 && l1_pt<100 && met_pt<100 && l2_pt<100 && genboson_pt<200 && event<2000000'
#visualCuts += ' && (mt<10 || (mt>50 && mt<60))'
canvas = ROOT.TCanvas('canvas', 'canvas', 2000, 1000)
#tree.Draw("mt:met_pt:abs(delta_phi_l1_met):abs(delta_phi_l2_met):abs(delta_phi_l1_l2):delta_eta_l1_l2",cuts+" && "+visualCuts,"para");
tree.Draw("genboson_pt:(l1_pt-met_pt)/(l1_pt+met_pt):abs(delta_phi_l2_met):mt",cuts+" && "+visualCuts,"para");
para = ROOT.gPad.GetListOfPrimitives().FindObject("ParaCoord");
para.__class__ = ROOT.TParallelCoord
para.SetAxisHistogramHeight(0.1)
#para.SetDotsSpacing(1)
#para.SetWeightCut(50000)
#l1_pt = para.GetVarList().FindObject("l1_pt");
#l1_pt.__class__ = ROOT.TParallelCoordVar
#l1_pt.AddRange(ROOT.TParallelCoordRange(l1_pt,0.,100));
#mt = para.GetVarList().FindObject("mt");
#mt.__class__ = ROOT.TParallelCoordVar
#range20 = ROOT.TParallelCoordRange(mt,0.,20)
#range40 = ROOT.TParallelCoordRange(mt,20.,40)
#range20.SetLineColor(ROOT.kViolet)
#range40.SetLineColor(ROOT.kBlue)
#mt.AddRange(range20);
#mt.AddRange(range40);
mt = para.GetVarList().FindObject("mt");
mt.__class__ = ROOT.TParallelCoordVar
genboson_pt = para.GetVarList().FindObject("genboson_pt");
genboson_pt.__class__ = ROOT.TParallelCoordVar
#
mt_range = [0,100]
nsteps = 50
#draw_steps = []
#draw_steps.extend(range(40,50))
#draw_steps.extend(range(25,28))
mt_bin = (mt_range[1]-mt_range[0])/nsteps
#ROOT.gStyle.SetPalette(56)
ncolors = ROOT.gStyle.GetNumberOfColors()
ranges = []
for i in xrange(nsteps):
    #if not i in draw_steps: continue
    min = mt_range[1]-(i+1)*mt_bin
    max = mt_range[1]-i*mt_bin
    para.AddSelection("mt_{MIN}_{MAX}".format(MIN=min,MAX=max));
    para.GetCurrentSelection().SetLineColor(ROOT.TColor.GetColorPalette(i*ncolors/nsteps));
    mt.AddRange(ROOT.TParallelCoordRange(mt,min,max))
#
#genboson_pt_range = [0,100]
#nsteps = 50
#genboson_pt_bin = (genboson_pt_range[1]-genboson_pt_range[0])/nsteps
#ranges = []
#for i in xrange(nsteps):
    #min = genboson_pt_range[0]+i*genboson_pt_bin
    #max = genboson_pt_range[0]+(i+1)*genboson_pt_bin
    ##min = genboson_pt_range[1]-(i+1)*genboson_pt_bin
    ##max = genboson_pt_range[1]-i*genboson_pt_bin
    #para.AddSelection("genboson_pt_{MIN}_{MAX}".format(MIN=min,MAX=max));
    #para.GetCurrentSelection().SetLineColor(ROOT.TColor.GetColorPalette(i*ncolors/nsteps));
    #genboson_pt.AddRange(ROOT.TParallelCoordRange(genboson_pt,min,max))
canvas.Print('plots/para.png')
