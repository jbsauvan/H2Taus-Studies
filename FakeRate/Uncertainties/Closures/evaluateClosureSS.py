from rootpy.plotting import Hist, Canvas
import ROOT
import Density
from Closure import Closure, plotClosure, plotSummary
import pickle

## load MC x-sections and sums of weights

mc_info = pickle.load(open('mc_info.pck', 'rb'))
int_lumi = 2094.2



closure_inputs = {
    'HighMTSS':{
        'Files':[
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/NonClosureSS/W/v_1_2016-03-03/fakerates_MuTau_W.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/NonClosureSS/TT/v_1_2016-03-03//fakerates_MuTau_TT.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/NonClosureSS/ZJ/v_1_2016-03-03//fakerates_MuTau_ZJ.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/NonClosureSS/T_tWch/v_1_2016-03-03//fakerates_MuTau_T_tWch.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/NonClosureSS/TBar_tWch/v_1_2016-03-03//fakerates_MuTau_TBar_tWch.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/NonClosureSS/VVTo2L2Nu/v_1_2016-03-03//fakerates_MuTau_VVTo2L2Nu.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/NonClosureSS/WZTo2L2Q/v_1_2016-03-03//fakerates_MuTau_WZTo2L2Q.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/NonClosureSS/WZTo3L/v_1_2016-03-03//fakerates_MuTau_WZTo3L.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/NonClosureSS/WZTo1L3Nu/v_1_2016-03-03//fakerates_MuTau_WZTo1L3Nu.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/NonClosureSS/WZTo1L1Nu2Q/v_1_2016-03-03//fakerates_MuTau_WZTo1L1Nu2Q.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/NonClosureSS/ZZTo2L2Q/v_1_2016-03-03//fakerates_MuTau_ZZTo2L2Q.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/NonClosureSS/WWTo1L1Nu2Q/v_1_2016-03-03//fakerates_MuTau_WWTo1L1Nu2Q.root',
        ],
        'Weights':[
            int_lumi*mc_info['W']['XSec']/mc_info['W']['SumWeights'],
            int_lumi*mc_info['TT']['XSec']/mc_info['TT']['SumWeights'],
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
        'TreeEst':'Weight_HighMTSS_Iso_Medium_VsPtDecay/ntFakeRate_MT40_InvertIso_Medium_tree',
    },
}


output_data = []
output_file = ROOT.TFile('./results/nonClosures_SS.root', 'RECREATE')

#mvis_bins = xrange(0, 400, 10)
#mvis_bins = [0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200., 225., 250., 275., 300., 325., 350., 375., 400., 450., 500., 550., 600.] 
mvis_bins = {
    #'Standard_x2':[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200,225,250,275,300,325,350],
    'Standard_x2':[0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200., 225., 250., 300., 350.],
    'Standard':[0., 20., 40., 60., 80., 100., 120., 140., 160., 180., 200., 250., 350.],
    'Standard_Div2':[0., 40., 80., 120., 160., 200., 350.],
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
    treeEst    = inputs['TreeEst']
    treeTrue   = inputs['TreeTrue']

    closure = Closure()
    closure.fillData('True', input_files, treeTrue, 'mvis', 'Weight', global_weights)
    closure.fillData('Est', input_files, treeEst, 'mvis', 'Weight', global_weights)

    closure.computeCDF('True')
    closure.computeCDF('Est')

    for name,bins in mvis_bins.items():
        plotClosure(fakeType+'_'+name, closure, bins, doErrors=True)

    #for nbins in [100,50,25]:
        #cdf = closure.data['True']['CDFInvert']
        #bins = [cdf.Eval(i/float(nbins)) for i in xrange(nbins+1)]
        #plotClosure(fakeType+'_NBins'+str(nbins), closure, bins)

    plotSummary(fakeType, closure, 0, 350)

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

