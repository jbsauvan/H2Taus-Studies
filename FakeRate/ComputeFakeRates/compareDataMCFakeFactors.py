import ROOT
import os
from EfficiencyPlots import DataMCEfficiencyPlot, PlotInfo
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.plotter.HistCreator import setSumWeights


inputDirectory = '../../../Histos/StudyFakeRate/MuMu/'
version = 'v_1_2016-01-26'
fileNameTemplate = 'fakerates_ZMuMu_{SAMPLE}.root'

dataSamples = [
    'Data_Run15D_05Oct',
    'Data_Run15D_v4',
]

mcSamples = [
    'Z',
    'QCD',
    'TBar_tWch',
    'TT',
    'T_tWch',
    'VVTo2L2Nu',
    'W',
    'WWTo1L1Nu2Q',
    'WZTo1L1Nu2Q',
    'WZTo1L3Nu',
    'WZTo2L2Q',
    'WZTo3L',
    'ZZTo2L2Q',
]


name = "FakeFactors_ZMuMu_DataMC"
plotDir = "plots/"

selections = [
    ('Iso_Medium', 'InvertIso_Medium')
]



variables = ["tau_pt"]
variableNames = {}
variableNames["tau_pt"] = "p_{T}^{#tau} [GeV]"

histoTemplate = 'hFakeRate_{SEL}_{VAR}'

## create list of file names
dataFileNames = []
mcFileNames = []
for sample in dataSamples:
    fileName = fileNameTemplate.format(SAMPLE=sample)
    dataFileNames.append('{DIR}/{SAMPLE}/{VERSION}/{FILE}'.format(DIR=inputDirectory,SAMPLE=sample,VERSION=version,FILE=fileName))
for sample in mcSamples:
    fileName = fileNameTemplate.format(SAMPLE=sample)
    mcFileNames.append('{DIR}/{SAMPLE}/{VERSION}/{FILE}'.format(DIR=inputDirectory,SAMPLE=sample,VERSION=version,FILE=fileName))


######################################
## Retrieve MC xsection normalization
cmgSampleTranslation = {
    'QCD':'QCD',
    'TBar_tWch':'TBar_tWch',
    'TT':'TT',
    'T_tWch':'T_tWch',
    'VVTo2L2Nu':'VVTo2L2Nu',
    'W':'W',
    'WWTo1L1Nu2Q':'WWTo1L1Nu2Q',
    'WZTo1L1Nu2Q':'WZTo1L1Nu2Q',
    'WZTo1L3Nu':'WZTo1L3Nu',
    'WZTo2L2Q':'WZTo2L2Q',
    'WZTo3L':'WZTo3L',
    'Z':'ZL',
    'ZZTo2L2Q':'ZZTo2L2Q',
}
int_lumi = 2094.2 # from Alexei's email
analysis_dir = '/afs/cern.ch/user/s/steggema/work/public/mm/190116/'
tree_prod_name = 'H2TauTauTreeProducerMuMu'
data_dir = analysis_dir
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, tree_prod_name=tree_prod_name)
for sample in all_samples:
    setSumWeights(sample)

mcRescalings = []
for sample in mcSamples:
    cmgName = cmgSampleTranslation[sample]
    mcRescalings.append(int_lumi*sampleDict[cmgName].xsec/sampleDict[cmgName].sumweights)
######################################



### define plot information
plotInfos = [PlotInfo(), PlotInfo(), PlotInfo()]
## Data
plotInfos[0].markerStyle = 20
plotInfos[0].yTitle = "Fake factor" 
plotInfos[0].legend = 'Data'
## MC
plotInfos[1].markerStyle = 20
plotInfos[1].markerColor = ROOT.kRed
plotInfos[1].lineColor = ROOT.kRed
plotInfos[1].yTitle = "Fake factor"
plotInfos[1].legend = 'MC'
## MC reference
plotInfos[2].markerStyle = 24
plotInfos[2].markerColor = ROOT.kRed
plotInfos[2].lineColor = ROOT.kRed
plotInfos[2].yTitle = "Fake factor"
plotInfos[2].legend = 'Z MC'

if not os.path.exists(plotDir+"/"+name):
    os.makedirs(plotDir+"/"+name)
outputFile = ROOT.TFile.Open(plotDir+"/"+name+"/"+name+".root", "RECREATE")

efficiencyPlots = []

for variable in variables:
    for selection in selections:
        effPlot = DataMCEfficiencyPlot()
        effPlot.name = '{NAME}_{PASS}_{REF}_{VAR}'.format(NAME=name,PASS=selection[0],REF=selection[1],VAR=variable)
        effPlot.plotDir = plotDir+'/'+name
        effPlot.selectionHistoName = histoTemplate.format(SEL=selection[0],VAR=variable)
        effPlot.referenceHistoName = histoTemplate.format(SEL=selection[1],VAR=variable)
        effPlot.dataFileNames = dataFileNames
        effPlot.mcFileNames = mcFileNames
        effPlot.mcRescalings = mcRescalings
        effPlot.referenceMC = True
        effPlot.dataPlotInfo = plotInfos[0]
        effPlot.mcPlotInfo = plotInfos[1]
        effPlot.referencePlotInfo = plotInfos[2]
        effPlot.outputFile = outputFile
        effPlot.divideOption = "pois"
        #effPlot.rebin = 2
        effPlot.plot(0., 0.3)
        efficiencyPlots.append(effPlot)


outputFile.Close()
