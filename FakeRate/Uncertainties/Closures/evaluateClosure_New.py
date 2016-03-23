import ROOT
from Closure_NoRootPy import Closure, plotClosure, plotSummary
import pickle
import copy

## load MC x-sections and sums of weights

mc_info = pickle.load(open('mc_info.pck', 'rb'))
int_lumi = 2094.2

ff_ss = ROOT.MakeNullPointer( "FakeFactor" ) 
ff_os = ROOT.MakeNullPointer( "FakeFactor" ) 

ff_file = ROOT.TFile.Open('/afs/cern.ch/user/j/jsauvan/workspace/Projects/Htautau_Run2/CMSSW/CMSSW_7_6_3/src/HTTutilities/Jet2TauFakes/test/fakeFactor_QCDOSSS15.root')
ff_file.GetObject('ff_qcd_ss', ff_ss)
ff_file.GetObject('ff_qcd_os', ff_os)

cuts = ["l1_muonid_medium>0.5","l1_pt>19"]
cuts.extend(["l2_againstMuon3>1.5","l2_againstElectronMVA5>0.5"])
cuts.extend(["veto_dilepton<0.5", "veto_thirdlepton<0.5", "veto_otherlepton<0.5"])
cuts.extend(["l2_decayModeFinding"])
cuts.extend(["l2_pt>20"])
cuts.extend(['mt<40'])
cuts.extend(['!(met_pt < 0.15 && met_phi > 0. && met_phi < 1.8)'])

cut_ss = ["l1_charge*l2_charge>0"]
cut_os = ["l1_charge*l2_charge<0"]

cut_muiso = ['l1_reliso05<0.10']
cut_muantiiso = ['l1_reliso05>0.15']
cut_mumediumiso1 = ['l1_reliso05>0.10', 'l1_reliso05<0.15']
cut_mumediumiso2 = ['l1_reliso05>0.05', 'l1_reliso05<0.15']
cut_mumediumiso3 = ['l1_reliso05>0.01', 'l1_reliso05<0.15']

cut_tauiso = ['l2_byCombinedIsolationDeltaBetaCorr3Hits >= 2']
cut_tauantiiso = ['l2_byCombinedIsolationDeltaBetaCorr3Hits < 2']

files = [
            # Data
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/SingleMuon_Run2015D_05Oct/H2TauTauTreeProducerTauMu/tree.root',
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/SingleMuon_Run2015D_v4/H2TauTauTreeProducerTauMu/tree.root',
            # Contamination
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/WJetsToLNu_LO/H2TauTauTreeProducerTauMu/tree.root',
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/DYJetsToLL_M50_LO/H2TauTauTreeProducerTauMu/tree.root',
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/TT_pow_ext/H2TauTauTreeProducerTauMu/tree.root',
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/T_tWch/H2TauTauTreeProducerTauMu/tree.root',
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/TBar_tWch/H2TauTauTreeProducerTauMu/tree.root',
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/VVTo2L2Nu/H2TauTauTreeProducerTauMu/tree.root',
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/WZTo2L2Q/H2TauTauTreeProducerTauMu/tree.root',
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/WZTo1L3Nu/H2TauTauTreeProducerTauMu/tree.root',
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/WZTo3L/H2TauTauTreeProducerTauMu/tree.root',
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/WZTo1L1Nu2Q/H2TauTauTreeProducerTauMu/tree.root',
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/ZZTo2L2Q/H2TauTauTreeProducerTauMu/tree.root',
            '/afs/cern.ch/user/j/jsauvan/workspace/public/HTauTau/Trees/mt/151215/WWTo1L1Nu2Q/H2TauTauTreeProducerTauMu/tree.root',
        ]

weights = [
            # Data
            1,1,
            # Subtract contamination
            -int_lumi*mc_info['W']['XSec']          /mc_info['W']['SumWeights'],
            -int_lumi*mc_info['ZJ']['XSec']         /mc_info['ZJ']['SumWeights'],
            -int_lumi*mc_info['TT']['XSec']         /mc_info['TT']['SumWeights'],
            -int_lumi*mc_info['T_tWch']['XSec']     /mc_info['T_tWch']['SumWeights'],
            -int_lumi*mc_info['TBar_tWch']['XSec']  /mc_info['TBar_tWch']['SumWeights'],
            -int_lumi*mc_info['VVTo2L2Nu']['XSec']  /mc_info['VVTo2L2Nu']['SumWeights'],
            -int_lumi*mc_info['WZTo2L2Q']['XSec']   /mc_info['WZTo2L2Q']['SumWeights'],
            -int_lumi*mc_info['WZTo1L3Nu']['XSec']  /mc_info['WZTo1L3Nu']['SumWeights'],
            -int_lumi*mc_info['WZTo3L']['XSec']     /mc_info['WZTo3L']['SumWeights'],
            -int_lumi*mc_info['WZTo1L1Nu2Q']['XSec']/mc_info['WZTo1L1Nu2Q']['SumWeights'],
            -int_lumi*mc_info['ZZTo2L2Q']['XSec']   /mc_info['ZZTo2L2Q']['SumWeights'],
            -int_lumi*mc_info['WWTo1L1Nu2Q']['XSec']/mc_info['WWTo1L1Nu2Q']['SumWeights'],
        ]

closure_inputs = {
    ## SS fake factors
    'FFSS_QCD_SS_MuAntiIso':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_ss+cut_muantiiso+cut_tauiso,
        'CutsAntiIso':cuts+cut_ss+cut_muantiiso+cut_tauantiiso,
        'FakeFactor':ff_ss,
    },
    'FFSS_QCD_SS_MuIso':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_ss+cut_muiso+cut_tauiso,
        'CutsAntiIso':cuts+cut_ss+cut_muiso+cut_tauantiiso,
        'FakeFactor':ff_ss,
    },
    'FFSS_QCD_SS_MuMediumIso10':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_ss+cut_mumediumiso1+cut_tauiso,
        'CutsAntiIso':cuts+cut_ss+cut_mumediumiso1+cut_tauantiiso,
        'FakeFactor':ff_ss,
    },
    'FFSS_QCD_SS_MuMediumIso05':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_ss+cut_mumediumiso2+cut_tauiso,
        'CutsAntiIso':cuts+cut_ss+cut_mumediumiso2+cut_tauantiiso,
        'FakeFactor':ff_ss,
    },
    'FFSS_QCD_SS_MuMediumIso01':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_ss+cut_mumediumiso3+cut_tauiso,
        'CutsAntiIso':cuts+cut_ss+cut_mumediumiso3+cut_tauantiiso,
        'FakeFactor':ff_ss,
    },
    'FFSS_QCD_OS_MuAntiIso':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_os+cut_muantiiso+cut_tauiso,
        'CutsAntiIso':cuts+cut_os+cut_muantiiso+cut_tauantiiso,
        'FakeFactor':ff_ss,
    },
    'FFSS_QCD_OS_MuMediumIso10':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_os+cut_mumediumiso1+cut_tauiso,
        'CutsAntiIso':cuts+cut_os+cut_mumediumiso1+cut_tauantiiso,
        'FakeFactor':ff_ss,
    },
    'FFSS_QCD_OS_MuMediumIso05':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_os+cut_mumediumiso2+cut_tauiso,
        'CutsAntiIso':cuts+cut_os+cut_mumediumiso2+cut_tauantiiso,
        'FakeFactor':ff_ss,
    },
    ## OS fake factors
    'FFOS_QCD_SS_MuAntiIso':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_ss+cut_muantiiso+cut_tauiso,
        'CutsAntiIso':cuts+cut_ss+cut_muantiiso+cut_tauantiiso,
        'FakeFactor':ff_os,
    },
    'FFOS_QCD_SS_MuIso':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_ss+cut_muiso+cut_tauiso,
        'CutsAntiIso':cuts+cut_ss+cut_muiso+cut_tauantiiso,
        'FakeFactor':ff_os,
    },
    'FFOS_QCD_SS_MuMediumIso10':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_ss+cut_mumediumiso1+cut_tauiso,
        'CutsAntiIso':cuts+cut_ss+cut_mumediumiso1+cut_tauantiiso,
        'FakeFactor':ff_os,
    },
    'FFOS_QCD_SS_MuMediumIso05':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_ss+cut_mumediumiso2+cut_tauiso,
        'CutsAntiIso':cuts+cut_ss+cut_mumediumiso2+cut_tauantiiso,
        'FakeFactor':ff_os,
    },
    'FFOS_QCD_SS_MuMediumIso01':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_ss+cut_mumediumiso3+cut_tauiso,
        'CutsAntiIso':cuts+cut_ss+cut_mumediumiso3+cut_tauantiiso,
        'FakeFactor':ff_os,
    },
    'FFOS_QCD_OS_MuAntiIso':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_os+cut_muantiiso+cut_tauiso,
        'CutsAntiIso':cuts+cut_os+cut_muantiiso+cut_tauantiiso,
        'FakeFactor':ff_os,
    },
    'FFOS_QCD_OS_MuMediumIso10':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_os+cut_mumediumiso1+cut_tauiso,
        'CutsAntiIso':cuts+cut_os+cut_mumediumiso1+cut_tauantiiso,
        'FakeFactor':ff_os,
    },
    'FFOS_QCD_OS_MuMediumIso05':{
        'Files':files,
        'Weights':weights,
        'Tree':'tree',
        'CutsIso':cuts+cut_os+cut_mumediumiso2+cut_tauiso,
        'CutsAntiIso':cuts+cut_os+cut_mumediumiso2+cut_tauantiiso,
        'FakeFactor':ff_os,
    },
}



def toString(cuts):
    string = ''
    for cut in cuts:
        string += cut
        string += ' && '
    string = string[:-3]
    return string


output_data = []
output_file = ROOT.TFile('./results_New/nonClosures.root', 'RECREATE')

#mvis_bins = xrange(0, 400, 10)
#mvis_bins = [0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200., 225., 250., 275., 300., 325., 350., 375., 400., 450., 500., 550., 600.] 
mvis_bins = {
    'Standard_x2':[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200,225,250,275,300,325,350,400,450],
    'Standard':[0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200., 225., 250., 300., 350., 450.],
    'Standard_Div2':[0., 20., 40., 60., 80., 100., 120., 140., 160., 180., 200., 250., 450.],
    #'Standard_Div4':[0., 40., 80., 120., 160., 200., 350., 600.],
}


nominal = 'Standard'


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



def writeNonClosure(closure, output, name):
    histoId = str(hash(str(mvis_bins[nominal])))
    clos = closure.data['True/Est']['Histo_{H}_Smooth'.format(H=histoId)]
    clos.SetName(name)
    output.cd()
    clos.Write()



setPlotStyle()
for fakeType,inputs in closure_inputs.items():
    input_files = inputs['Files']
    global_weights = inputs['Weights']
    tree   = inputs['Tree']
    fakefactor = inputs['FakeFactor']
    cuts_true = inputs['CutsIso']
    cuts_est = inputs['CutsAntiIso']

    closure = Closure()
    closure.fillData('True', input_files, tree, 'mvis', toString(cuts_true), 'weight', global_weights)
    closure.fillData('Est', input_files, tree, 'mvis', toString(cuts_est), 'weight', global_weights, fakefactor=fakefactor, ffInputs=['l2_pt', 'l2_decayMode'])

    closure.computeCDF('True')
    closure.computeCDF('Est')

    for name,bins in mvis_bins.items():
        plotClosure(fakeType+'_'+name, closure, bins, doErrors=False, yRange=[0.5,2.])

    #for nbins in [100,50,25]:
        #cdf = closure.data['True']['CDFInvert']
        #bins = [cdf.Eval(i/float(nbins)) for i in xrange(nbins+1)]
        #plotClosure(fakeType+'_NBins'+str(nbins), closure, bins)

    plotSummary(fakeType, closure, 0, 600)

    #
    writeNonClosure(closure, output_file, '{FAKETYPE}_Histo_Smooth_Ratio'.format(FAKETYPE=fakeType))

    #canvas.Write()
    ##cdfTrue.SetName('{FAKETYPE}_CDF_True'.format(FAKETYPE=fakeType))
    ##cdfEst.SetName('{FAKETYPE}_CDF_Est'.format(FAKETYPE=fakeType))
    #histoTrue.SetName('{FAKETYPE}_Histo_True_{H}'.format(FAKETYPE=fakeType,H=binid))
    #histoEst.SetName('{FAKETYPE}_Histo_Est_{H}'.format(FAKETYPE=fakeType,H=binid))
    #histoDiff.SetName('{FAKETYPE}_Histo_Diff_{H}'.format(FAKETYPE=fakeType,H=binid))
    #histoSmoothDiff.SetName('{FAKETYPE}_Histo_Smooth_Diff_{H}'.format(FAKETYPE=fakeType,H=binid))
    #histoRatio.SetName('{FAKETYPE}_Histo_Ratio_{H}'.format(FAKETYPE=fakeType,H=binid))
    #histoSmoothRatio.SetName('{FAKETYPE}_Histo_Smooth_Ratio_{H}'.format(FAKETYPE=fakeType,H=binid))
    #histoSmoothRatioError.SetName('{FAKETYPE}_Histo_SmoothError_Ratio_{H}'.format(FAKETYPE=fakeType,H=binid))
    ##cdfTrue.Write()
    ##cdfEst.Write()
    #histoTrue.Write()
    #histoEst.Write()
    #histoDiff.Write()
    #histoSmoothDiff.Write()
    #histoRatio.Write()
    #histoSmoothRatio.Write()
    #histoSmoothRatioError.Write()
    ##
    ##output_data.append(cdfTrue)
    ##output_data.append(cdfEst)
    #output_data.append(histoTrue)
    #output_data.append(histoEst)
    #output_data.append(histoDiff)
    #output_data.append(histoSmoothDiff)
    #output_data.append(histoRatio)
    #output_data.append(histoSmoothRatio)
    #output_data.append(histoSmoothRatioError)


output_file.Close()
ff_file.Close()

