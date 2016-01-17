import ROOT
from VariableCorrelations import VariableCorrelations


inputFile = ROOT.TFile.Open('/afs/cern.ch/work/s/steggema/public/mt/18112015/WJetsToLNu_LO/H2TauTauTreeProducerTauMu/tree.root')
tree = inputFile.Get('tree')

cuts = ''
cuts += 'l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19'
cuts += ' && l2_againstMuon3>1.5 && l2_againstElectronMVA5>0.5 && l2_decayModeFinding'
cuts += ' && veto_dilepton<0.5 && veto_thirdlepton<0.5 && veto_otherlepton<0.5'
cuts += ' && l2_decayModeFinding && l2_pt>20 && l2_gen_match==6'
#
cuts += ' && mt<100'
cuts += ' && l2_pt<150'
cuts += ' && l2_jet_pt<150'
cuts += ' && met_pt<100'
cuts += ' && genmet_pt<100'
cuts += ' && genboson_pt<200'
cuts += ' && l2_byCombinedIsolationDeltaBetaCorrRaw3Hits<100'
cuts += ' && sqrt(2.*l1_gen_pt*genmet_pt*(1.-cos(genmet_phi-l1_gen_phi)))<100'
#cuts += ' && genboson_pt*cosh(genboson_eta)<400'
#
cutIso = 'l2_byCombinedIsolationDeltaBetaCorr3Hits>=2'
cutInvertIso = 'l2_byCombinedIsolationDeltaBetaCorr3Hits<2'
cutOS = 'l1_charge*l2_charge<0'
cutSS = 'l1_charge*l2_charge>0'
#
mtbinCuts = ['mt<20', 'mt>20 && mt<40', 'mt>40 && mt<60', 'mt>60']

variables = []
variables.append('mt')
variables.append('sqrt(2.*l1_gen_pt*genmet_pt*(1.-cos(genmet_phi-l1_gen_phi)))') ## gen  MT
#variables.append('mvis')
variables.append('met_pt')
variables.append('genmet_pt')
variables.append('((met_pt-genmet_pt)/genmet_pt<1. ? (met_pt-genmet_pt)/genmet_pt : 1)')
variables.append('l1_pt')
variables.append('l1_gen_pt')
variables.append('(l1_pt-met_pt)/(l1_pt+met_pt)')
variables.append('(l1_gen_pt-genmet_pt)/(l1_gen_pt+genmet_pt)')
variables.append('l2_pt')
#variables.append('met_phi')
#variables.append('genmet_phi')
#variables.append('l1_phi')
#variables.append('l1_gen_phi')
variables.append('abs(delta_phi_l1_met)')
variables.append('abs(TVector2::Phi_mpi_pi(l1_gen_phi-genmet_phi))')
variables.append('abs(delta_phi_l2_met)')
variables.append('abs(delta_phi_l1_l2)')
#variables.append('abs(delta_eta_l1_l2)')
#variables.append('abs(l1_eta)')
#variables.append('abs(l2_eta)')
#variables.append('l2_mass')
#variables.append('l2_decayMode')
variables.append('l2_byCombinedIsolationDeltaBetaCorrRaw3Hits')
#variables.append('l2_chargedIsoPtSum')
#variables.append('l2_neutralIsoPtSum')
#variables.append('l2_puCorrPtSum')
#variables.append('l2_nc_ratio')
#variables.append('l2_gen_pdgId')
#variables.append('l2_photonPtSumOutsideSignalCone')
variables.append('genboson_pt')
#variables.append('genboson_pt*cosh(genboson_eta)')
#variables.append('abs(genboson_eta)')
#variables.append('abs(genboson_eta)')
variables.append('(l2_jet_pt>0?l2_jet_pt:0)')

enable = []
enable.append('mt')
enable.append('mvis')
enable.append('met_pt')
enable.append('l1_pt')
enable.append('l2_pt')
enable.append('met_phi')
enable.append('l1_phi')
enable.append('delta_phi_l1_met')
enable.append('delta_phi_l2_met')
enable.append('delta_phi_l1_l2')
enable.append('delta_eta_l1_l2')
enable.append('l2_eta')
enable.append('l1_eta')
enable.append('l2_mass')
enable.append('l2_decayMode')
enable.append('l2_byCombinedIsolationDeltaBetaCorrRaw3Hits')
enable.append('l2_chargedIsoPtSum')
enable.append('l2_neutralIsoPtSum')
enable.append('l2_puCorrPtSum')
enable.append('l2_nc_ratio')
enable.append('l2_gen_pdgId')
enable.append('l2_photonPtSumOutsideSignalCone')
enable.append('genboson_pt')
enable.append('genboson_eta')
enable.append('l1_gen_pt')
enable.append('l1_gen_phi')
enable.append('genmet_pt')
enable.append('genmet_phi')
enable.append('l2_jet_pt')


variableNames = {}
for var in variables:
    variableNames[var] = var
variableNames['sqrt(2.*l1_gen_pt*genmet_pt*(1.-cos(genmet_phi-l1_gen_phi)))'] = 'gen_mt'
variableNames['(l1_pt-met_pt)/(l1_pt+met_pt)'] = 'met_l1_asymm'
variableNames['(l1_gen_pt-genmet_pt)/(l1_gen_pt+genmet_pt)'] = 'gen_met_l1_asymm'
#variableNames['(met_pt-genmet_pt)/genmet_pt'] = 'met_mismeasure'
variableNames['((met_pt-genmet_pt)/genmet_pt<1. ? (met_pt-genmet_pt)/genmet_pt : 1)'] = 'met_mismeasure'
variableNames['(jet1_pt>0?jet1_pt:0)'] = 'jet1_pt'
variableNames['(jet2_pt>0?jet2_pt:0)'] = 'jet2_pt'
variableNames['(l2_jet_pt>0?l2_jet_pt:0)'] = 'l2_jet_pt'
variableNames['delta_phi_l1_met'] = 'delta_phi_l2_met' ## swaped l1 and l2 variables in the trees
variableNames['delta_phi_l2_met'] = 'delta_phi_l1_met'
variableNames['abs(TVector2::Phi_mpi_pi(l1_gen_phi-genmet_phi))'] = 'delta_phi_gen_l1_met'
variableNames['genboson_pt*cosh(genboson_eta)'] = 'genboson_p'
variableNames['abs(genboson_eta)'] = 'genboson_eta'

legends = {}
legends['mt'] = 'm_{T}'
legends['sqrt(2.*l1_gen_pt*genmet_pt*(1.-cos(genmet_phi-l1_gen_phi)))'] = 'm_{T}^{gen}'
legends['met_pt'] = 'MET'
legends['genmet_pt'] = 'MET^{gen}'
legends['l1_pt'] = 'p_{T}^{#mu}'
legends['l1_gen_pt'] = 'p_{T}^{#mu}^{gen}'
legends['(l1_pt-met_pt)/(l1_pt+met_pt)'] = '(p_{T}^{#mu}-MET)/(p_{T}^{#mu}+MET)'
legends['(l1_gen_pt-genmet_pt)/(l1_gen_pt+genmet_pt)'] = '(p_{T}^{#mu}^{gen}-MET^{gen})/(p_{T}^{#mu}^{gen}+MET^{gen})'
legends['l2_pt'] = 'p_{T}^{#tau}'
legends['met_phi'] = '#Phi^{MET}'
legends['genmet_phi'] = '#Phi^{MET,gen}'
legends['l1_phi'] = '#Phi^{#mu}'
legends['l1_gen_phi'] = '#Phi^{#mu,gen}'
legends['abs(delta_phi_l1_met)'] = '#Delta#Phi(#tau,MET)' ## swaped l1 and l2 variables in the trees
legends['abs(delta_phi_l2_met)'] = '#Delta#Phi(#mu,MET)'
legends['abs(TVector2::Phi_mpi_pi(l1_gen_phi-genmet_phi))'] = '#Delta#Phi(#mu,MET)^{gen}'
legends['abs(delta_phi_l1_l2)'] = '#Delta#Phi(#mu,#tau)'
legends['l2_byCombinedIsolationDeltaBetaCorrRaw3Hits'] = 'iso'
legends['genboson_pt'] = 'p_{T}^{W,gen}'
legends['(l2_jet_pt>0?l2_jet_pt:0)'] = 'p_{T}^{jet}'
legends['(met_pt-genmet_pt)/genmet_pt'] = '(MET-MET^{gen})/MET^{gen}'
legends['((met_pt-genmet_pt)/genmet_pt<1. ? (met_pt-genmet_pt)/genmet_pt : 1)'] = '(MET-MET^{gen})/MET^{gen}'
legends['genboson_pt*cosh(genboson_eta)'] = 'p^{W}'
legends['abs(genboson_eta)'] = '|#eta^{W}|'


scatterPlotVariables = ['mt', 'sqrt(2.*l1_gen_pt*genmet_pt*(1.-cos(genmet_phi-l1_gen_phi)))', 'l2_byCombinedIsolationDeltaBetaCorrRaw3Hits', 'genboson_pt', '(l2_jet_pt>0?l2_jet_pt:0)']
#scatterPlotPairs = [('genmet_pt','met_pt'), ('l1_gen_pt','l1_pt'), ('l1_gen_phi','l1_phi'), ('genmet_phi','met_phi')]
scatterPlotPairs = []


correlations = VariableCorrelations()
correlations.variable_list.extend(variables)
correlations.enable_list.extend(enable)
correlations.legends = legends
correlations.readTree(tree, cuts)
correlations.plotCorrelations('wjets_mt_correlations')
for var2 in variables:
    for var1 in scatterPlotVariables:
        if var2!=var1:
            correlations.plotDependency('wjets_dependency_{VAR1}_{VAR2}'.format(VAR1=variableNames[var1],VAR2=variableNames[var2]), var1, var2, 100, 100)
    for var1,var2 in scatterPlotPairs:
        correlations.plotDependency('wjets_dependency_{VAR1}_{VAR2}'.format(VAR1=variableNames[var1],VAR2=variableNames[var2]), var1, var2, 100, 100)

for i,mtbincut in enumerate(mtbinCuts):
    correlations.data = []
    correlations.readTree(tree, cuts+' && '+mtbincut)
    correlations.plotCorrelations('wjets_mtbin{}_correlations'.format(i))
    for var2 in variables:
        for var1 in scatterPlotVariables:
            if var2!=var1:
                correlations.plotDependency('wjets_mtbin{I}_dependency_{VAR1}_{VAR2}'.format(I=i,VAR1=variableNames[var1],VAR2=variableNames[var2]), var1, var2, 100, 100)
    for var1,var2 in scatterPlotPairs:
        correlations.plotDependency('wjets_mtbin{I}_dependency_{VAR1}_{VAR2}'.format(I=i,VAR1=variableNames[var1],VAR2=variableNames[var2]), var1, var2, 100, 100)

#correlations.data = []
#correlations.readTree(tree, cuts+' && '+cutIso+' && '+cutOS)
#correlations.plotCorrelations('wjets_Iso_OS_mt_correlations')
#for var in variables:
    #if var!='mt':
        #correlations.plotDependency('wjets_Iso_OS_dependency', 'mt', var, 100, 100)

#correlations.data = []
#correlations.readTree(tree, cuts+' && '+cutInvertIso+' && '+cutOS)
#correlations.plotCorrelations('wjets_InvertIso_OS_mt_correlations')
#for var in variables:
    #if var!='mt':
        #correlations.plotDependency('wjets_InvertIso_OS_dependency', 'mt', var, 100, 100)


