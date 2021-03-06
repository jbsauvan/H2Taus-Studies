import ROOT
from BinByBinCorrelations import CorrelationMatrix

## Input files and histograms
histoDir = "../../../Histos/StudyFakeRate/MuTau/FakeFactorUncertaintiesFromToys/"
version = "v_1_2016-02-23"
samples = ["W", "TT", "QCD", "ZJ"]

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
for name,sys in systematics.items():
    for i in xrange(200):
        sys.append(["{NAME}_Fluctuate{I}".format(NAME=name,I=i)])

#systematics = []
#for i in xrange(200):
    #systematics.append(["Weight_Iso_Medium_VsPt_Fluctuate{}".format(i)])


#nominal  = 'Weight_Iso_Medium_VsPt'


plots = []
canvas = []
for name,sys in systematics.items():
    for sample,histo in histos.items():
        plots.append(CorrelationMatrix())
        plots[-1].inputFiles = [ROOT.TFile.Open(h[0]) for h in histo]
        plots[-1].histoNames = [h[1] for h in histo]
        plots[-1].name = "mvis_"+sample+'_'+name+'_200'
        plots[-1].title = "m_{vis} [GeV]"
        #plots[-1].plotNumbers = True
        plots[-1].plotDir = 'plots/correlations/'
        plots[-1].sysNames = sys[0:200]
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
