import ROOT
import os
import copy
from EfficiencyPlots import DataMCEfficiencyPlot, PlotInfo
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.plotter.HistCreator import setSumWeights


inputDirectory = '../../../Histos/StudyFakeRate/MuTau_FakeRateWJetsHighMT/'
version = 'v_3_2016-01-29'
fileNameTemplate = 'fakerates_MuTau_WJetsHighMT_{SAMPLE}.root'

dataSamples = [
    'Data_Run15D_05Oct',
    'Data_Run15D_v4',
]

mcSamples = [
    'W',
    'Z',
    'QCD',
    'TBar_tWch',
    'TT',
    'T_tWch',
    'VVTo2L2Nu',
    'WWTo1L1Nu2Q',
    'WZTo1L1Nu2Q',
    'WZTo1L3Nu',
    'WZTo2L2Q',
    'WZTo3L',
    'ZZTo2L2Q',
]


name = "FakeFactors_HighMT_DataMC"
plotDir = "plots/"

selections = [
    ('Iso_Medium', 'InvertIso_Medium')
]



variables = ["tau_pt", 'tau_jet_pt', "tau_decayMode"]
variableNames = {}
variableNames["tau_pt"] = "p_{T}^{#tau} [GeV]"
variableNames["tau_jet_pt"] = "p_{T}^{jet} [GeV]"
variableNames["tau_decayMode"] = "decayMode"

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
analysis_dir = '/afs/cern.ch/user/s/steggema/work/public/mt/151215/'
tree_prod_name = 'H2TauTauTreeProducerTauMu'
data_dir = analysis_dir
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, tree_prod_name=tree_prod_name)
for sample in all_samples:
    setSumWeights(sample, directory='MCWeighter')

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
plotInfos[2].legend = 'W MC'

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
        effPlot.dataPlotInfo = copy.deepcopy(plotInfos[0])
        effPlot.mcPlotInfo = copy.deepcopy(plotInfos[1])
        effPlot.referencePlotInfo = copy.deepcopy(plotInfos[2])
        effPlot.dataPlotInfo.xTitle = variableNames[variable]
        effPlot.mcPlotInfo.xTitle = variableNames[variable]
        effPlot.referencePlotInfo.xTitle = variableNames[variable]
        effPlot.outputFile = outputFile
        effPlot.divideOption = "pois"
        #effPlot.rebin = 2
        effPlot.plot(0., 0.3)
        efficiencyPlots.append(effPlot)


outputFile.Close()
