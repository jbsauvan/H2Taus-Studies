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
cuts += ' && met_pt<100'
cuts += ' && genboson_pt<200'
cuts += ' && l2_byCombinedIsolationDeltaBetaCorrRaw3Hits<100'
cuts += ' && l2_gen_pt<200'
#
cutIso = 'l2_byCombinedIsolationDeltaBetaCorr3Hits>=2'
cutInvertIso = 'l2_byCombinedIsolationDeltaBetaCorr3Hits<2'
cutOS = 'l1_charge*l2_charge<0'
cutSS = 'l1_charge*l2_charge>0'
#
mtbinCuts = ['mt<20', 'mt>20 && mt<40', 'mt>40 && mt<60', 'mt>60']

variables = []
variables.append('mt')
#variables.append('mvis')
variables.append('met_pt')
variables.append('l1_pt')
variables.append('(l1_pt-met_pt)/(l1_pt+met_pt)')
variables.append('l2_pt')
variables.append('abs(delta_phi_l1_met)')
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
#variables.append('abs(genboson_eta)')
variables.append('(l2_gen_pt>0?l2_gen_pt:0)')

enable = []
enable.append('mt')
enable.append('mvis')
enable.append('met_pt')
enable.append('l1_pt')
enable.append('l2_pt')
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
enable.append('l2_gen_pt')

variableNames = {}
for var in variables:
    variableNames[var] = var
variableNames['(l1_pt-met_pt)/(l1_pt+met_pt)'] = 'met_l1_asymm'
variableNames['(jet1_pt>0?jet1_pt:0)'] = 'jet1_pt'
variableNames['(jet2_pt>0?jet2_pt:0)'] = 'jet2_pt'
variableNames['(l2_gen_pt>0?l2_gen_pt:0)'] = 'l2_gen_pt'

legends = {}
legends['mt'] = 'm_{T}'
legends['met_pt'] = 'MET'
legends['l1_pt'] = 'p_{T}^{#mu}'
legends['(l1_pt-met_pt)/(l1_pt+met_pt)'] = '(p_{T}^{#mu}-MET)/(p_{T}^{#mu}+MET)'
legends['l2_pt'] = 'p_{T}^{#tau}'
legends['abs(delta_phi_l1_met)'] = '#Delta#Phi(#mu,MET)'
legends['abs(delta_phi_l2_met)'] = '#Delta#Phi(#tau,MET)'
legends['abs(delta_phi_l1_l2)'] = '#Delta#Phi(#mu,#tau)'
legends['l2_byCombinedIsolationDeltaBetaCorrRaw3Hits'] = 'iso'
legends['genboson_pt'] = 'p_{T}^{W,gen}'
legends['(l2_gen_pt>0?l2_gen_pt:0)'] = 'p_{T}^{jet,gen}'


scatterPlotVariables = ['mt', 'l2_byCombinedIsolationDeltaBetaCorrRaw3Hits', 'genboson_pt', '(l2_gen_pt>0?l2_gen_pt:0)']


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

for i,mtbincut in enumerate(mtbinCuts):
    correlations.data = []
    correlations.readTree(tree, cuts+' && '+mtbincut)
    correlations.plotCorrelations('wjets_mtbin{}_correlations'.format(i))
    for var2 in variables:
        for var1 in scatterPlotVariables:
            if var2!=var1:
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


