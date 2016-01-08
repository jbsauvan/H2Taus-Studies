import ROOT
from BinByBinCorrelations import CorrelationMatrix

## Input files and histograms
histoDir = "../../../Histos/StudyFakeRate/MuTau_Stat/"
version = "v_2_2016-01-08"
samples = ["W", "TT", "QCD", "ZJ"]

histos = {}
for sample in samples:
    histos[sample] = ["{DIR}/{SAMPLE}/{VERSION}/fakerates_MuTau_Stat_{SAMPLE}.root".format(DIR=histoDir,SAMPLE=sample,VERSION=version), "hFakeRate_MT40_InvertIso_Medium_mvis_vs_match5"]

systematics = []
for i in xrange(100):
    systematics.append(["Weight_Iso_Medium_VsPt_Fluctuate{}".format(i)])


nominal  = 'Weight_Iso_Medium_VsPt'


plots = []
canvas = []
for sample,histo in histos.items():
    plots.append(CorrelationMatrix())
    plots[-1].inputFile = ROOT.TFile.Open(histo[0])
    plots[-1].histoName = histo[1]
    plots[-1].name = "mvis_"+sample+'_100'
    plots[-1].title = "m_{vis} [GeV]"
    #plots[-1].plotNumbers = True
    plots[-1].plotDir = 'plots/correlations/'
    plots[-1].sysNames = systematics
    plots[-1].nomName = nominal
    plots[-1].retrieveHistos()
    plots[-1].computeShifts()
    plots[-1].computeCorrelationMatrix()
    canvas.append(plots[-1].plot())
    plots[-1].inputFile.Close()

for sample,histo in histos.items():
    plots.append(CorrelationMatrix())
    plots[-1].inputFile = ROOT.TFile.Open(histo[0])
    plots[-1].histoName = histo[1]
    plots[-1].name = "mvis_"+sample+'_50'
    plots[-1].title = "m_{vis} [GeV]"
    #plots[-1].plotNumbers = True
    plots[-1].plotDir = 'plots/correlations/'
    plots[-1].sysNames = systematics[0:50]
    plots[-1].nomName = nominal
    plots[-1].retrieveHistos()
    plots[-1].computeShifts()
    plots[-1].computeCorrelationMatrix()
    canvas.append(plots[-1].plot())
    plots[-1].inputFile.Close()

for sample,histo in histos.items():
    plots.append(CorrelationMatrix())
    plots[-1].inputFile = ROOT.TFile.Open(histo[0])
    plots[-1].histoName = histo[1]
    plots[-1].name = "mvis_"+sample+'_10'
    plots[-1].title = "m_{vis} [GeV]"
    #plots[-1].plotNumbers = True
    plots[-1].plotDir = 'plots/correlations/'
    plots[-1].sysNames = systematics[0:10]
    plots[-1].nomName = nominal
    plots[-1].retrieveHistos()
    plots[-1].computeShifts()
    plots[-1].computeCorrelationMatrix()
    canvas.append(plots[-1].plot())
    plots[-1].inputFile.Close()

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
