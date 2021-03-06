from rootpy.plotting import Hist, Canvas
import ROOT
import Density
from Closure import Closure, plotClosure, plotSummary
import pickle
from array import array

## load MC x-sections and sums of weights




closure_inputs = {
    'HighMTRaw':{
        'Files':[
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/W/v_5_2016-02-10/fakerates_MuTau_W.root',
        ],
        'Weights':[
            1,
        ],
        'TreeTrue':'ntFakeRate_Iso_Medium_tree',
        'TreeEst':'Weight_HighMTRaw_Iso_Medium_VsPtDecay/ntFakeRate_InvertIso_Medium_tree',
    },
}


output_data = []
output_file = ROOT.TFile('./results/mtCorrections.root', 'RECREATE')

mt_bins = {
    'Standard_x2':[0.,5,10.,15,20.,25,30.,35,40.,45,50.,55,60.,65,70.,75,80.,85,90.,95,100.,110, 120.,130, 140.,155, 170.,200., 250.],
    'Standard':[0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 120., 140., 170.,200., 250.],
    'Standard_Div2':[0., 20., 40., 60., 80., 100., 140.,200., 250.],
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


def forceLowMTLinearDistance(closure, name):
    cdf = closure.data[name]['CDF']
    invcdf = closure.data[name]['CDFInvert']
    value50 = invcdf.Eval(0.5)
    print value50
    for p in xrange(cdf.GetN()):
        if cdf.GetX()[p]>=value50: continue
        cdf.SetPoint(p, cdf.GetX()[p], cdf.GetX()[p]*0.5/value50)
        invcdf.SetPoint(p, cdf.GetX()[p]*0.5/value50, cdf.GetX()[p])
        print cdf.GetX()[p], cdf.GetX()[p]*0.5/value50

def writeCorrectionAnderrors(closure, output):
    histoId = str(hash(str(mt_bins[nominal])))
    corr = closure.data['True/Est']['Histo_{H}_Smooth'.format(H=histoId)]
    corrStatErr = closure.data['True/Est']['Histo_{H}_SmoothError'.format(H=histoId)]
    xs = []
    ysup = []
    ysdown = []
    ysbinup = []
    ysbindown = []
    for p in xrange(corr.GetN()):
        nom = corr.GetY()[p]
        up = corrStatErr.GetY()[p]
        down = nom - (up-nom)
        xs.append(corr.GetX()[p])
        ysup.append(up)
        ysdown.append(down)
        binup = 0
        bindown = 0
        for name,graph in closure.data['True/Est'].items():
            if 'Histo' in name and 'Smooth' in name and not 'Error' in name:
                diff = graph.GetY()[p] - nom
                if diff>binup: binup = diff
                if diff<bindown: bindown = diff
        ysbinup.append(nom+binup)
        ysbindown.append(nom+bindown)
    #
    graphup = ROOT.TGraphAsymmErrors(corr.GetN(), array('f', xs), array('f',ysup), array('f',[0]*corr.GetN()), array('f',[0]*corr.GetN()), array('f',[0]*corr.GetN()), array('f',[0]*corr.GetN())) 
    graphdown = ROOT.TGraphAsymmErrors(corr.GetN(), array('f', xs), array('f',ysdown), array('f',[0]*corr.GetN()), array('f',[0]*corr.GetN()), array('f',[0]*corr.GetN()), array('f',[0]*corr.GetN())) 
    graphbinup = ROOT.TGraphAsymmErrors(corr.GetN(), array('f', xs), array('f',ysbinup), array('f',[0]*corr.GetN()), array('f',[0]*corr.GetN()), array('f',[0]*corr.GetN()), array('f',[0]*corr.GetN())) 
    graphbindown = ROOT.TGraphAsymmErrors(corr.GetN(), array('f', xs), array('f',ysbindown), array('f',[0]*corr.GetN()), array('f',[0]*corr.GetN()), array('f',[0]*corr.GetN()), array('f',[0]*corr.GetN()))
    corr.SetName('mt_correction')
    graphup.SetName('mt_correction_statup')
    graphdown.SetName('mt_correction_statdown')
    graphbinup.SetName('mt_correction_binup')
    graphbindown.SetName('mt_correction_bindown')
    output.cd()
    corr.Write()
    graphup.Write()
    graphdown.Write()
    graphbinup.Write()
    graphbindown.Write()


setPlotStyle()
for fakeType,inputs in closure_inputs.items():
    input_files = inputs['Files']
    global_weights = inputs['Weights']
    treeEst    = inputs['TreeEst']
    treeTrue   = inputs['TreeTrue']

    closure = Closure()
    closure.fillData('True', input_files, treeTrue, 'mt', 'Weight', global_weights)
    closure.fillData('Est', input_files, treeEst, 'mt', 'Weight', global_weights)

    closure.computeCDF('True')
    closure.computeCDF('Est')
    forceLowMTLinearDistance(closure, 'True')
    forceLowMTLinearDistance(closure, 'Est')


    for name,bins in mt_bins.items():
        plotClosure(fakeType+'_'+name, closure, bins, smoothWidth=0.1, kernelDistance='Adapt', doErrors=True, xTitle='m_{T} [GeV]')

    #for nbins in [100,50,25]:
        #cdf = closure.data['True']['CDFInvert']
        #bins = [cdf.Eval(i/float(nbins)) for i in xrange(nbins+1)]
        #plotClosure(fakeType+'_NBins'+str(nbins), closure, bins)

    plotSummary(fakeType, closure, 0, 250, xTitle='m_{T} [GeV]')

    output_file.cd()
    writeCorrectionAnderrors(closure, output_file)
    #closure.data['True']['CDF'].Write()
    #closure.data['Est']['CDF'].Write()


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

