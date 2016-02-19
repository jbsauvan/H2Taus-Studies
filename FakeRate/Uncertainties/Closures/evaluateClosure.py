from rootpy.plotting import Hist, Canvas
import ROOT
import Density
from Closure import Closure
import pickle

## load MC x-sections and sums of weights

mc_info = pickle.load(open('mc_info.pck', 'rb'))
int_lumi = 2094.2



closure_inputs = {
    'HighMT':{
        'Files':[
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/W/v_5_2016-02-10/fakerates_MuTau_W.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/TT/v_5_2016-02-10/fakerates_MuTau_TT.root'
        ],
        'Weights':[
            int_lumi*mc_info['W']['XSec']/mc_info['W']['SumWeights'],
            int_lumi*mc_info['TT']['XSec']/mc_info['TT']['SumWeights'],
        ],
        'TreeTrue':'ntFakeRate_MT40_Iso_Medium_tree',
        'TreeEst':'Weight_HighMT_Iso_Medium_VsPtDecay/ntFakeRate_MT40_InvertIso_Medium_tree',
    },
    #'QCDSS':{
        #'File':'/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/QCD/v_5_2016-02-10/fakerates_MuTau_QCD.root',
        #'TreeTrue':'ntFakeRate_MT40_Iso_Medium_tree',
        #'TreeEst':'Weight_QCDSS_Iso_Medium_VsPtDecay/ntFakeRate_MT40_InvertIso_Medium_tree',
    #},
    'QCDSS':{
        'Files':[
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/QCDFakeFactorClosure/Data_Run15D_v4/v_1_2016-02-17/fakerates_MuTau_Data_Run15D_v4.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/QCDFakeFactorClosure/Data_Run15D_05Oct/v_1_2016-02-17/fakerates_MuTau_Data_Run15D_05Oct.root',
        ],
        'Weights':[1,1],
        'TreeTrue':'ntFakeRate_MT40_Iso_Medium_tree',
        'TreeEst':'Weight_QCDSS_Iso_Medium_VsPtDecay/ntFakeRate_MT40_InvertIso_Medium_tree',
    },
    'ZMuMu':{
        'Files':[
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/ZJ/v_5_2016-02-10/fakerates_MuTau_ZJ.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/T_tWch/v_5_2016-02-10/fakerates_MuTau_T_tWch.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/TBar_tWch/v_5_2016-02-10/fakerates_MuTau_TBar_tWch.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/VVTo2L2Nu/v_5_2016-02-10/fakerates_MuTau_VVTo2L2Nu.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/WZTo2L2Q/v_5_2016-02-10/fakerates_MuTau_WZTo2L2Q.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/WZTo3L/v_5_2016-02-10/fakerates_MuTau_WZTo3L.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/WZTo1L3Nu/v_5_2016-02-10/fakerates_MuTau_WZTo1L3Nu.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/WZTo1L1Nu2Q/v_5_2016-02-10/fakerates_MuTau_WZTo1L1Nu2Q.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/ZZTo2L2Q/v_5_2016-02-10/fakerates_MuTau_ZZTo2L2Q.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/WWTo1L1Nu2Q/v_5_2016-02-10/fakerates_MuTau_WWTo1L1Nu2Q.root',
        ],
        'Weights':[
            int_lumi*mc_info['ZJ']['XSec']         /mc_info['ZJ']['SumWeights'],
            int_lumi*mc_info['T_tWch']['XSec']     /mc_info['T_tWch']['SumWeights'],
            int_lumi*mc_info['TBar_tWch']['XSec']  /mc_info['TBar_tWch']['SumWeights'],
            int_lumi*mc_info['VVTo2L2Nu']['XSec']  /mc_info['VVTo2L2Nu']['SumWeights'],
            int_lumi*mc_info['WZTo2L2Q']['XSec']   /mc_info['WZTo2L2Q']['SumWeights'],
            int_lumi*mc_info['WZTo3L']['XSec']     /mc_info['WZTo3L']['SumWeights'],
            int_lumi*mc_info['WZTo1L3Nu']['XSec']  /mc_info['WZTo1L3Nu']['SumWeights'],
            int_lumi*mc_info['WZTo1L1Nu2Q']['XSec']/mc_info['WZTo1L1Nu2Q']['SumWeights'],
            int_lumi*mc_info['ZZTo2L2Q']['XSec']   /mc_info['ZZTo2L2Q']['SumWeights'],
            int_lumi*mc_info['WWTo1L1Nu2Q']['XSec']/mc_info['WWTo1L1Nu2Q']['SumWeights'],
        ],
        'TreeTrue':'ntFakeRate_MT40_Iso_Medium_tree',
        'TreeEst':'Weight_Iso_Medium_VsPtDecay/ntFakeRate_MT40_InvertIso_Medium_tree',
    },
}


output_data = []
output_file = ROOT.TFile('./results/nonClosures.root', 'RECREATE')

#mvis_bins = xrange(0, 400, 10)
#mvis_bins = [0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200., 225., 250., 275., 300., 325., 350., 375., 400., 450., 500., 550., 600.] 
mvis_bins = [0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200., 225., 250., 300., 350., 450., 600.] 


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


setPlotStyle()
for fakeType,inputs in closure_inputs.items():
    input_files = inputs['Files']
    global_weights = inputs['Weights']
    treeEst    = inputs['TreeEst']
    treeTrue   = inputs['TreeTrue']

    closure = Closure()
    closure.fillData('True', input_files, treeTrue, 'mvis', 'Weight', global_weights)
    closure.fillData('Est', input_files, treeEst, 'mvis', 'Weight', global_weights)

    #closure.computeTKDE('True', mvis_bins[0], mvis_bins[-1])
    #closure.computeTKDE('Est', mvis_bins[0], mvis_bins[-1])
    closure.computeCDF('True')
    closure.computeCDF('Est')
    closure.computeHisto('True', mvis_bins)
    closure.computeHisto('Est', mvis_bins)
    #closure.computeDiff('True', 'Est', 'TKDE')
    closure.computeDiff('True', 'Est', 'Histo')
    #closure.computeRatio('Est', 'True', 'TKDE')
    closure.computeRatio('Est', 'True', 'Histo', smoothWidth=0.1)

    closure.clearData()

    #graphTrue = closure.data['True']['TKDE']
    #graphEst  = closure.data['Est']['TKDE']
    cdfTrue = closure.data['True']['CDF']
    cdfEst  = closure.data['Est']['CDF']
    histoTrue = closure.data['True']['Histo']
    histoEst  = closure.data['Est']['Histo']

    #graphDiff = closure.data['Est-True']['TKDE']
    histoDiff = closure.data['Est-True']['Histo']
    histoSmoothDiff = closure.data['Est-True']['Histo_Smooth']
    #graphRatio = closure.data['True/Est']['TKDE']
    histoRatio = closure.data['True/Est']['Histo']
    histoSmoothRatio = closure.data['True/Est']['Histo_Smooth']


    ############ plot raw distributions
    histoDummy = Hist(1, mvis_bins[0],  mvis_bins[-1], type='F')
    values = []
    values.append(histoTrue.GetMaximum())
    values.append(histoTrue.GetMinimum())
    values.append(histoEst.GetMaximum())
    values.append(histoEst.GetMinimum())
    maxi = max(values)*1.1
    mini = min(values)
    histoDummy.SetAxisRange(mini, maxi, 'Y')
    ##
    histoTrue.SetMarkerColor(ROOT.kBlack)
    histoEst.SetMarkerStyle(24)
    histoEst.SetMarkerColor(ROOT.kGray+3)
    ##
    canvas = Canvas(800, 800)
    canvas.SetName('{FAKETYPE}_Canvas'.format(FAKETYPE=fakeType))
    histoDummy.SetXTitle('m_{vis} [GeV]')
    histoDummy.SetYTitle('Events')
    histoDummy.Draw()
    histoTrue.Draw('same')
    histoEst.Draw('same')
    legend = ROOT.TLegend(0.4,0.7,0.9,0.9)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.AddEntry(histoTrue, 'True background', 'lp')
    legend.AddEntry(histoEst, 'Estimated background', 'lp')
    legend.Draw()
    canvas.Print('results/{FAKETYPE}_NonClosure.png'.format(FAKETYPE=fakeType))


    ################ Plot ratios
    histoDummy2 = Hist(1, mvis_bins[0],  mvis_bins[-1], type='F')
    values = []
    values.append(histoRatio.GetMaximum())
    values.append(histoRatio.GetMinimum())
    #values.append(histoSmoothRatio.GetMaximum())
    #values.append(histoSmoothRatio.GetMinimum())
    maxi = max(values)
    mini = min(values)
    maxi = maxi*1.1 if maxi>0 else maxi*0.9
    mini = mini*1.1 if mini<0 else mini*0.9
    histoDummy2.SetAxisRange(mini, maxi, 'Y')
    ##
    histoRatio.SetMarkerColor(ROOT.kBlack)
    histoSmoothRatio.SetLineColor(ROOT.kGray+3)
    histoSmoothRatio.SetLineWidth(3)
    ##
    canvas2 = Canvas(800, 800)
    canvas2.SetName('{FAKETYPE}_Ratio_Canvas'.format(FAKETYPE=fakeType))
    histoDummy2.SetXTitle('m_{vis} [GeV]')
    histoDummy2.SetYTitle('Ratio')
    histoDummy2.Draw()
    histoRatio.Draw('same')
    histoSmoothRatio.Draw('l same')
    canvas2.Print('results/{FAKETYPE}_NonClosure_Ratio.png'.format(FAKETYPE=fakeType))
    #
    output_file.cd()
    canvas.Write()
    #graphTrue.SetName('{FAKETYPE}_KDE_True'.format(FAKETYPE=fakeType))
    #graphEst.SetName('{FAKETYPE}_KDE_Est'.format(FAKETYPE=fakeType))
    #graphDiff.SetName('{FAKETYPE}_KDE_Diff'.format(FAKETYPE=fakeType))
    #graphRatio.SetName('{FAKETYPE}_KDE_Ratio'.format(FAKETYPE=fakeType))
    cdfTrue.SetName('{FAKETYPE}_CDF_True'.format(FAKETYPE=fakeType))
    cdfEst.SetName('{FAKETYPE}_CDF_Est'.format(FAKETYPE=fakeType))
    histoTrue.SetName('{FAKETYPE}_Histo_True'.format(FAKETYPE=fakeType))
    histoEst.SetName('{FAKETYPE}_Histo_Est'.format(FAKETYPE=fakeType))
    histoDiff.SetName('{FAKETYPE}_Histo_Diff'.format(FAKETYPE=fakeType))
    histoSmoothDiff.SetName('{FAKETYPE}_Histo_Smooth_Diff'.format(FAKETYPE=fakeType))
    histoRatio.SetName('{FAKETYPE}_Histo_Ratio'.format(FAKETYPE=fakeType))
    histoSmoothRatio.SetName('{FAKETYPE}_Histo_Smooth_Ratio'.format(FAKETYPE=fakeType))
    #graphTrue.Write()
    #graphEst.Write()
    #graphDiff.Write()
    #graphRatio.Write()
    cdfTrue.Write()
    cdfEst.Write()
    histoTrue.Write()
    histoEst.Write()
    histoDiff.Write()
    histoSmoothDiff.Write()
    histoRatio.Write()
    histoSmoothRatio.Write()
    #
    #output_data.append(graphTrue)
    #output_data.append(graphEst)
    #output_data.append(graphDiff)
    #output_data.append(graphRatio)
    output_data.append(cdfTrue)
    output_data.append(cdfEst)
    output_data.append(histoTrue)
    output_data.append(histoEst)
    output_data.append(histoDiff)
    output_data.append(histoSmoothDiff)
    output_data.append(histoRatio)
    output_data.append(histoSmoothRatio)


output_file.Close()

