import ROOT
from VariableCorrelations import VariableCorrelations


inputFile = ROOT.TFile.Open('/afs/cern.ch/work/s/steggema/public/mt/18112015/WJetsToLNu_LO/H2TauTauTreeProducerTauMu/tree.root')
tree = inputFile.Get('tree')

cuts = ''
cuts += 'l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19'
cuts += ' && l2_againstMuon3>1.5 && l2_againstElectronMVA5>0.5 && l2_decayModeFinding'
cuts += ' && veto_dilepton<0.5 && veto_thirdlepton<0.5 && veto_otherlepton<0.5'
cuts += ' && l2_decayModeFinding && l2_pt>20 && l2_gen_match==6'
#cuts += ' && mt>40'
cutIso = 'l2_byCombinedIsolationDeltaBetaCorr3Hits>=2'
cutInvertIso = 'l2_byCombinedIsolationDeltaBetaCorr3Hits<2'
cutOS = 'l1_charge*l2_charge<0'
cutSS = 'l1_charge*l2_charge>0'

variables = []
variables.append('mt')
variables.append('mvis')
variables.append('met_pt')
variables.append('l1_pt')
variables.append('l2_pt')
variables.append('l2_eta')
variables.append('l2_mass')
variables.append('l2_decayMode')
variables.append('l2_byCombinedIsolationDeltaBetaCorrRaw3Hits')
variables.append('l2_chargedIsoPtSum')
variables.append('l2_neutralIsoPtSum')
variables.append('l2_puCorrPtSum')
variables.append('l2_nc_ratio')
variables.append('l2_gen_pdgId')
variables.append('l2_photonPtSumOutsideSignalCone')

correlations = VariableCorrelations()
correlations.variable_list.extend(variables)
correlations.readTree(tree, cuts)
correlations.plotCorrelations('wjets_mt_correlations')
for var in variables:
    if var!='mt':
        correlations.plotDependency('wjets_dependency', 'mt', var, 100, 100)

correlations.data = []
correlations.readTree(tree, cuts+' && '+cutIso+' && '+cutOS)
correlations.plotCorrelations('wjets_Iso_OS_mt_correlations')
for var in variables:
    if var!='mt':
        correlations.plotDependency('wjets_Iso_OS_dependency', 'mt', var, 100, 100)

correlations.data = []
correlations.readTree(tree, cuts+' && '+cutInvertIso+' && '+cutOS)
correlations.plotCorrelations('wjets_InvertIso_OS_mt_correlations')
for var in variables:
    if var!='mt':
        correlations.plotDependency('wjets_InvertIso_OS_dependency', 'mt', var, 100, 100)


