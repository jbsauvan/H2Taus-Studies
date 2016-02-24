import ROOT
from BinByBinCorrelations import CorrelationMatrix

## Input files and histograms
histoDir = "../../../Histos/StudyFakeRate/MuTau/FakeFactorUncertainties/"
version = "v_5_2016-02-19"
samples = {
    'Data':['Data_Run15D_05Oct','Data_Run15D_v4']
}

histos = {}
for name,sample in samples.items():
    histos[name] = []
    for s in sample:
        histos[name].append(["{DIR}/{SAMPLE}/{VERSION}/fakerates_MuTau_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=s,VERSION=version), "hFakeRate_MT40_InvertIso_Medium_mvis_stdbins"])

systematics = {
    'Weight_Combined_Iso_Medium_VsPtDecay':[],
}
## Retrieve all shifted fake factors in the input files
for name,sys in systematics.items():
    f = ROOT.TFile.Open(histos['Data'][0][0])
    keys = f.GetListOfKeys()
    upsys = []
    downsys = []
    for key in keys:
        if key.IsFolder() and 'ShiftStat' in key.GetName():
            if 'Up' in key.GetName() and not key.GetName() in upsys: 
                upsys.append(key.GetName())
            if 'Down' in key.GetName() and not key.GetName() in downsys: 
                downsys.append(key.GetName())
    for us in upsys:
        ds = us.replace('Up','Down')
        if not ds in downsys:
            print 'WARNING: Cannot find down sys corresponding to '+us
        else:
            sys.append([us,ds])


#nominal  = 'Weight_Iso_Medium_VsPt'


plots = []
canvas = []
for name,sys in systematics.items():
    for sample,histo in histos.items():
        plots.append(CorrelationMatrix())
        plots[-1].inputFiles = [ROOT.TFile.Open(h[0]) for h in histo]
        plots[-1].histoNames = [h[1] for h in histo]
        plots[-1].name = "mvis_"+sample+'_'+name+'_statShifts'
        plots[-1].title = "m_{vis} [GeV]"
        #plots[-1].plotNumbers = True
        plots[-1].plotDir = 'plots/correlations/'
        plots[-1].sysNames = sys
        plots[-1].nomName = name
        plots[-1].retrieveHistos()
        plots[-1].computeShifts()
        plots[-1].computeCorrelationMatrix()
        canvas.append(plots[-1].plot())
        for f in plots[-1].inputFiles: f.Close()

#canvas = []
#for plot in plots:
    #plot.plotDir = 'plots/correlations/'
    #plot.sysNames = systematics
    #plot.nomName = nominal
    #plot.retrieveHistos()
    #plot.computeShifts()
    #plot.computeCorrelationMatrix()
    #canvas.append(plot.plot())
    #plot.inputFile.Close()
