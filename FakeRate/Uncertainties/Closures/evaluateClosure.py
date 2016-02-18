from rootpy.plotting import Hist, Canvas
import ROOT
import Density
from Closure import Closure


closure_inputs = {
    'HighMT':{
        'File':'/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/W/v_5_2016-02-10/fakerates_MuTau_W.root',
        'TreeTrue':'ntFakeRate_MT40_Iso_Medium_tree',
        'TreeEst':'Weight_HighMT_Iso_Medium_VsPtDecay/ntFakeRate_MT40_InvertIso_Medium_tree',
    },
    #'QCDSS':{
        #'File':'/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/QCD/v_5_2016-02-10/fakerates_MuTau_QCD.root',
        #'TreeTrue':'ntFakeRate_MT40_Iso_Medium_tree',
        #'TreeEst':'Weight_QCDSS_Iso_Medium_VsPtDecay/ntFakeRate_MT40_InvertIso_Medium_tree',
    #},
    'QCDSS':{
        'File':[
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/QCDFakeFactorClosure/Data_Run15D_v4/v_1_2016-02-17/fakerates_MuTau_Data_Run15D_v4.root',
            '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/QCDFakeFactorClosure/Data_Run15D_05Oct/v_1_2016-02-17/fakerates_MuTau_Data_Run15D_05Oct.root',
        ],
        'TreeTrue':'ntFakeRate_MT40_Iso_Medium_tree',
        'TreeEst':'Weight_QCDSS_Iso_Medium_VsPtDecay/ntFakeRate_MT40_InvertIso_Medium_tree',
    },
    'ZMuMu':{
        'File':'/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Histos/StudyFakeRate/MuTau/AllFakeFactors/TT/v_5_2016-02-10/fakerates_MuTau_TT.root',
        'TreeTrue':'ntFakeRate_MT40_Iso_Medium_tree',
        'TreeEst':'Weight_Iso_Medium_VsPtDecay/ntFakeRate_MT40_InvertIso_Medium_tree',
    },
}


output_data = []
output_file = ROOT.TFile('./results/nonClosures.root', 'RECREATE')

for fakeType,inputs in closure_inputs.items():
    input_file = inputs['File']
    treeEst    = inputs['TreeEst']
    treeTrue   = inputs['TreeTrue']

    closure = Closure()
    closure.fillData('True', input_file, treeTrue, 'mvis', 'Weight')
    closure.fillData('Est', input_file, treeEst, 'mvis', 'Weight')

    closure.computeTKDE('True')
    closure.computeTKDE('Est')
    closure.computeHisto('True')
    closure.computeHisto('Est')
    closure.computeDiff('True', 'Est', 'TKDE')
    closure.computeDiff('True', 'Est', 'Histo')
    closure.computeRatio('Est', 'True', 'TKDE')
    closure.computeRatio('Est', 'True', 'Histo')

    closure.clearData()

    graphTrue = closure.data['True']['TKDE']
    graphEst  = closure.data['Est']['TKDE']
    histoTrue = closure.data['True']['Histo']
    histoEst  = closure.data['Est']['Histo']

    graphDiff = closure.data['Est-True']['TKDE']
    histoDiff = closure.data['Est-True']['Histo']
    histoSmoothDiff = closure.data['Est-True']['Histo_Smooth']
    graphRatio = closure.data['True/Est']['TKDE']
    histoRatio = closure.data['True/Est']['Histo']
    histoSmoothRatio = closure.data['True/Est']['Histo_Smooth']


    histoDummy = Hist(1, 0, 250, type='F')
    ys = graphTrue.GetY()
    ys.SetSize(graphTrue.GetN())
    values = list(ys)
    ys = graphEst.GetY()
    ys.SetSize(graphEst.GetN())
    values.extend(list(ys))
    diffs = graphDiff.GetY()
    diffs.SetSize(graphDiff.GetN())
    values.extend(list(diffs))
    values.append(histoTrue.GetMaximum())
    values.append(histoTrue.GetMinimum())
    values.append(histoEst.GetMaximum())
    values.append(histoEst.GetMinimum())
    values.append(histoDiff.GetMaximum())
    values.append(histoDiff.GetMinimum())
    maxi = max(values)*1.1
    mini = min(values)
    histoDummy.SetAxisRange(mini, maxi, 'Y')
    #
    graphTrue.SetLineColor(ROOT.kRed)
    graphEst.SetLineColor(ROOT.kBlue)
    histoTrue.SetMarkerColor(ROOT.kRed)
    histoEst.SetMarkerColor(ROOT.kBlue)
    #
    canvas = Canvas(800, 800)
    canvas.SetName('{FAKETYPE}_Canvas'.format(FAKETYPE=fakeType))
    histoDummy.Draw()
    graphTrue.Draw('same')
    graphEst.Draw('same')
    histoTrue.Draw('same')
    histoEst.Draw('same')
    graphDiff.Draw('same')
    histoDiff.Draw('same')
    histoSmoothDiff.Draw('hist same')
    canvas.Print('results/{FAKETYPE}_NonClosure.png'.format(FAKETYPE=fakeType))
    #
    output_file.cd()
    canvas.Write()
    graphTrue.SetName('{FAKETYPE}_KDE_True'.format(FAKETYPE=fakeType))
    graphEst.SetName('{FAKETYPE}_KDE_Est'.format(FAKETYPE=fakeType))
    graphDiff.SetName('{FAKETYPE}_KDE_Diff'.format(FAKETYPE=fakeType))
    graphRatio.SetName('{FAKETYPE}_KDE_Ratio'.format(FAKETYPE=fakeType))
    histoTrue.SetName('{FAKETYPE}_Histo_True'.format(FAKETYPE=fakeType))
    histoEst.SetName('{FAKETYPE}_Histo_Est'.format(FAKETYPE=fakeType))
    histoDiff.SetName('{FAKETYPE}_Histo_Diff'.format(FAKETYPE=fakeType))
    histoSmoothDiff.SetName('{FAKETYPE}_Histo_Smooth_Diff'.format(FAKETYPE=fakeType))
    histoRatio.SetName('{FAKETYPE}_Histo_Ratio'.format(FAKETYPE=fakeType))
    histoSmoothRatio.SetName('{FAKETYPE}_Histo_Smooth_Ratio'.format(FAKETYPE=fakeType))
    graphTrue.Write()
    graphEst.Write()
    graphDiff.Write()
    graphRatio.Write()
    histoTrue.Write()
    histoEst.Write()
    histoDiff.Write()
    histoSmoothDiff.Write()
    histoRatio.Write()
    histoSmoothRatio.Write()
    #
    output_data.append(graphTrue)
    output_data.append(graphEst)
    output_data.append(graphDiff)
    output_data.append(graphRatio)
    output_data.append(histoTrue)
    output_data.append(histoEst)
    output_data.append(histoDiff)
    output_data.append(histoSmoothDiff)
    output_data.append(histoRatio)
    output_data.append(histoSmoothRatio)


output_file.Close()

