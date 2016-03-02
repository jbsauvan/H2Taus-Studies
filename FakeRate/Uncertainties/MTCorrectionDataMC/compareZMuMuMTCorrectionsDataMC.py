from rootpy.plotting import Hist, Canvas
import ROOT
import Density
from Closure import Closure, plotClosure, plotSummary
import pickle
from array import array

## load MC x-sections and sums of weights




closure_inputs = {
    'Data':{
        'Files':[
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuMu_MTStudy/76X/Data_Run15D/v_1_2016-03-01/fakerates_ZMuMu_MTStudy_Data_Run15D.root',
        ],
        'Weights':[
            1,
        ],
        'TreeTrue':'ntFakeRate_Iso_Medium_tree',
        'TreeEst':'Weight_ZMuMu_HighMT_Iso_Medium_VsPtDecay/ntFakeRate_InvertIso_Medium_tree',
    },
    'MC':{
        'Files':[
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuMu_MTStudy/76X/Z/v_1_2016-03-01/fakerates_ZMuMu_MTStudy_Z.root',
        ],
        'Weights':[
            1,
        ],
        'TreeTrue':'ntFakeRate_Iso_Medium_tree',
        'TreeEst':'Weight_ZMuMu_HighMT_Iso_Medium_VsPtDecay/ntFakeRate_InvertIso_Medium_tree',
    },
}


output_data = []
output_file = ROOT.TFile('./results/zmumu_mtCorrections_datamc.root', 'RECREATE')

mt_bins = {
    #'Standard_x2':[0.,5,10.,15,20.,25,30.,35,40.,45,50.,55,60.,65,70.,75,80.,85,90.,95,100.,110, 120.,130, 140.,155, 170.,200., 250.],
    'Standard':[0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 120.],
    #'Standard_Div2':[0., 20., 40., 60., 80., 100., 140.,200., 250.],
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

def plotDataMC(name, closureData, closureMC, bins, xTitle='m_{vis} [GeV]'):
    binid = hash(str(bins))
    #
    histoRatioData = closureData.data['True/Est']['Histo_{H}'.format(H=binid)]
    histoSmoothRatioData = closureData.data['True/Est']['Histo_{H}_Smooth'.format(H=binid)]
    histoSmoothRatioErrorData = closureData.data['True/Est']['Histo_{H}_SmoothError'.format(H=binid)]
    histoRatioMC = closureMC.data['True/Est']['Histo_{H}'.format(H=binid)]
    histoSmoothRatioMC = closureMC.data['True/Est']['Histo_{H}_Smooth'.format(H=binid)]
    histoSmoothRatioErrorMC = closureMC.data['True/Est']['Histo_{H}_SmoothError'.format(H=binid)]
    #
    ################ Plot ratios
    histoDummyRatio = Hist(1, bins[0],  bins[-1], type='F')
    values = []
    values.append(histoRatioData.GetMaximum())
    values.append(histoRatioData.GetMinimum())
    values.append(histoRatioMC.GetMaximum())
    values.append(histoRatioMC.GetMinimum())
    maxi = max(values)
    mini = min(values)
    maxi = maxi*1.1 if maxi>0 else maxi*0.9
    mini = mini*1.1 if mini<0 else mini*0.9
    histoDummyRatio.SetAxisRange(mini, maxi, 'Y')
    ##
    histoRatioData.SetMarkerColor(ROOT.kBlack)
    histoSmoothRatioData.SetLineColor(ROOT.kGray+3)
    histoSmoothRatioData.SetLineWidth(2)
    histoSmoothRatioErrorData.SetLineColor(ROOT.kGray+1)
    histoSmoothRatioErrorData.SetFillColor(ROOT.kGray+1)
    ##
    histoRatioMC.SetMarkerColor(ROOT.kRed)
    histoRatioMC.SetMarkerStyle(21)
    histoSmoothRatioMC.SetLineColor(ROOT.kRed)
    histoSmoothRatioMC.SetLineWidth(2)
    histoSmoothRatioErrorMC.SetLineColor(ROOT.kRed-7)
    #histoSmoothRatioErrorMC.SetFillColorAlpha(ROOT.kRed-7, 0.35)
    histoSmoothRatioErrorMC.SetFillStyle(3344)
    histoSmoothRatioErrorMC.SetFillColor(ROOT.kRed-7)
    ##
    canvasRatio = Canvas(800, 800)
    canvasRatio.SetName('{NAME}_Ratio_Canvas'.format(NAME=name))
    histoDummyRatio.SetXTitle(xTitle)
    histoDummyRatio.SetYTitle('Ratio')
    histoDummyRatio.Draw()
    histoSmoothRatioErrorData.Draw('fl same')
    histoSmoothRatioData.Draw('pl same')
    histoSmoothRatioErrorMC.Draw('fl same')
    histoSmoothRatioMC.Draw('pl same')
    histoRatioData.Draw('E1 same')
    histoRatioMC.Draw('E1 same')
    #
    legend = ROOT.TLegend(0.15, 0.75, 0.45, 0.9)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.AddEntry(histoRatioMC, 'MC', 'lp')
    legend.AddEntry(histoRatioData, 'Data', 'lp')
    legend.Draw()
    canvasRatio.Print('results/{NAME}_NonClosure_Ratio.png'.format(NAME=name))


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

def writeCorrectionAnderrors(closure, name, output):
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
    corr.SetName(name+'_mt_correction')
    graphup.SetName(name+'_mt_correction_statup')
    graphdown.SetName(name+'_mt_correction_statdown')
    graphbinup.SetName(name+'_mt_correction_binup')
    graphbindown.SetName(name+'_mt_correction_bindown')
    output.cd()
    corr.Write()
    graphup.Write()
    graphdown.Write()
    graphbinup.Write()
    graphbindown.Write()


setPlotStyle()
closures = {}
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


    #plotSummary(fakeType, closure, 0, 250, xTitle='m_{T} [GeV]')

    output_file.cd()
    writeCorrectionAnderrors(closure, fakeType, output_file)
    closure.clearData()
    closures[fakeType] = closure
    #closure.data['True']['CDF'].Write()
    #closure.data['Est']['CDF'].Write()


plotDataMC('DataMC', closures['Data'], closures['MC'], mt_bins[nominal], xTitle='m_{T} [GeV]' )



output_file.Close()

