
import ROOT
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import TT_pow, DYJetsToLL_M50_LO, WJetsToLNu_LO, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, T_tWch, TBar_tWch, TToLeptons_tch_amcatnlo, TToLeptons_sch_amcatnlo

int_lumi = 1560.

histo_base_dir = '../../Histos/StudyFakeRate/MuTau/'
histo_version = 'v_1_2015-11-23'
histo_file_template_name = histo_base_dir+'/{SAMPLE}/'+histo_version+'/fakerates_MuTau_{SAMPLE}.root'
histo_template_name = '{DIR}hFakeRate_{SEL}_{VAR}'
sample_names = ['ZL','ZJ','W','TT','T_tWch','TBar_tWch','WW','WZ','ZZ','QCD']

cmgHistoFile = ROOT.TFile.Open("../../CMSSW/CMSSW_7_4_15/src/CMGTools/H2TauTau/plotting/mt/fakeplots/histos.root")

Name = "Name"
File = "File"
Histo = "Histo"
XSec = "XSec"
SumWeights = "SumWeights"

histo_configs = []
histo_configs.append({Name:'ZL'       , File:histo_file_template_name.format(SAMPLE='ZL')       , Histo:'', XSec:DYJetsToLL_M50_LO.xSection, SumWeights:DYJetsToLL_M50_LO.nGenEvents})
histo_configs.append({Name:'ZJ'       , File:histo_file_template_name.format(SAMPLE='ZJ')       , Histo:'', XSec:DYJetsToLL_M50_LO.xSection, SumWeights:DYJetsToLL_M50_LO.nGenEvents})
histo_configs.append({Name:'W'        , File:histo_file_template_name.format(SAMPLE='W')        , Histo:'', XSec:WJetsToLNu_LO.xSection    , SumWeights:WJetsToLNu_LO.nGenEvents    })
histo_configs.append({Name:'TT'       , File:histo_file_template_name.format(SAMPLE='TT')       , Histo:'', XSec:TT_pow.xSection           , SumWeights:TT_pow.nGenEvents           })
histo_configs.append({Name:'T_tWch'   , File:histo_file_template_name.format(SAMPLE='T_tWch')   , Histo:'', XSec:T_tWch.xSection           , SumWeights:T_tWch.nGenEvents           })
histo_configs.append({Name:'TBar_tWch', File:histo_file_template_name.format(SAMPLE='TBar_tWch'), Histo:'', XSec:TBar_tWch.xSection        , SumWeights:TBar_tWch.nGenEvents        })
histo_configs.append({Name:'ZZ'       , File:histo_file_template_name.format(SAMPLE='ZZ')       , Histo:'', XSec:ZZp8.xSection             , SumWeights:ZZp8.nGenEvents             })
histo_configs.append({Name:'WZ'       , File:histo_file_template_name.format(SAMPLE='WZ')       , Histo:'', XSec:WZp8.xSection             , SumWeights:WZp8.nGenEvents             })
histo_configs.append({Name:'WW'       , File:histo_file_template_name.format(SAMPLE='WW')       , Histo:'', XSec:WWTo2L2Nu.xSection        , SumWeights:WWTo2L2Nu.nGenEvents        })
histo_configs.append({Name:'QCD'      , File:histo_file_template_name.format(SAMPLE='QCD')      , Histo:'', XSec:QCD_Mu15.xSection         , SumWeights:1.                          })

### Signal region histo
# recomputed
signalRegionHisto = None
for config in histo_configs:
    config[Histo] = histo_template_name.format(DIR='',SEL='StandardIso',VAR='mvis')
    file = ROOT.TFile.Open(config[File])
    histo = file.Get(config[Histo])
    histo.__class__ = ROOT.TH1F
    histo.SetDirectory(0)
    file.Close()
    histo.Scale(int_lumi*config[XSec]/config[SumWeights])
    if not signalRegionHisto:
        signalRegionHisto = histo
    else:
        signalRegionHisto.Add(histo)


# From CMG
cmgSignalRegionHisto = cmgHistoFile.Get("hFakeRate_StandardIso_mvis")
cmgSignalRegionHisto.__class__ = ROOT.TH1F
cmgSignalRegionHisto.SetDirectory(0)


# Compare histos
nbins = cmgSignalRegionHisto.GetNbinsX()
for b in xrange(1,nbins+1):
    cmgValue = cmgSignalRegionHisto.GetBinContent(b)
    value = signalRegionHisto.GetBinContent(b)
    if value!=cmgValue:
        print value,'!=',cmgValue, '(', (abs(value-cmgValue)/value),')'


### Weighted histo
# recomputed
controlRegionHisto = None
for config in histo_configs:
    config[Histo] = histo_template_name.format(DIR='Weight_VsPt/',SEL='InvertIso',VAR='mvis')
    file = ROOT.TFile.Open(config[File])
    histo = file.Get(config[Histo])
    histo.__class__ = ROOT.TH1F
    histo.SetDirectory(0)
    file.Close()
    histo.Scale(int_lumi*config[XSec]/config[SumWeights])
    if not controlRegionHisto:
        controlRegionHisto = histo
    else:
        controlRegionHisto.Add(histo)

# From CMG
cmgControlRegionHisto = cmgHistoFile.Get("hFakeRate_InvertIso_mvis")
cmgControlRegionHisto.__class__ = ROOT.TH1F
cmgControlRegionHisto.SetDirectory(0)

# Compare histos
nbins = cmgControlRegionHisto.GetNbinsX()
for b in xrange(1,nbins+1):
    cmgValue = cmgControlRegionHisto.GetBinContent(b)
    value = controlRegionHisto.GetBinContent(b)
    if value!=cmgValue:
        print value,'!=',cmgValue, '(', (abs(value-cmgValue)/value),')'



cmgHistoFile.Close()
