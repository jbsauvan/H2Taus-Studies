import ROOT
import math
import shutil

histo_base_dir = '../../..//Histos/StudyFakeRate/MuTau/'
histo_version = 'v_10_2015-12-09'
histo_file_template_name = histo_base_dir+'/{SAMPLE}/'+histo_version+'/fakerates_MuTau_{SAMPLE}.root'
histo_template_name = '{DIR}hFakeRate_{SEL}_mvis_vs_match5' ## '_vs_match5' is for gen_match=6

uncertainty_file = ROOT.TFile.Open('./outputHistos/fakeFactorStatUncertainties.root')
uncertainty_histo_template_name = 'fakeUncertainty_{SAMPLE}_{FAKEFACTOR}'

selection = 'MT40_InvertIso_Medium'
#samples = ["W"]
samples = ["W", "TT", "QCD", "TBar_tWch", "T_tWch", "WW", "WZ", "ZJ", "ZZ"]
fakefactors= [
    'Weight_Iso_Medium_Inclusive',
    'Weight_Iso_Medium_VsPt',
    'Weight_Iso_Medium_VsDecay',
    'Weight_Iso_Medium_VsPtDecay',
]


for sample in samples:
    shutil.copy(histo_file_template_name.format(SAMPLE=sample), histo_file_template_name.format(SAMPLE=sample).replace('.root', '_FFStatUnc.root'))
    #inputFile = ROOT.TFile.Open(histo_file_template_name.format(SAMPLE=sample), 'update')
    inputFile = ROOT.TFile.Open(histo_file_template_name.format(SAMPLE=sample).replace('.root', '_FFStatUnc.root'), 'update')
    for fakefactor in fakefactors:
        inputHisto = inputFile.Get(histo_template_name.format(DIR=fakefactor+'/',SEL=selection))
        inputHisto.__class__ = ROOT.TH1F
        outputHisto = inputHisto.Clone(inputHisto.GetName()+'_FFStatUnc')
        uncertainty = uncertainty_file.Get(uncertainty_histo_template_name.format(SAMPLE=sample,FAKEFACTOR=fakefactor))
        uncertainty.__class__ = ROOT.TH1F
        nbins = outputHisto.GetNbinsX()
        for b in xrange(nbins+2): # includes overflows
            error = outputHisto.GetBinError(b)
            content = outputHisto.GetBinContent(b)
            ffError = uncertainty.GetBinContent(b)*content
            outputHisto.SetBinError(b, math.sqrt(error**2+ffError**2))
        inputFile.cd(fakefactor)
        outputHisto.Write()
    inputFile.Close()

uncertainty_file.Close()
