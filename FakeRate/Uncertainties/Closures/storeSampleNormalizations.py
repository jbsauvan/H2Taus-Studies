from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.plotter.HistCreator import setSumWeights
import pickle

analysis_dir = '/afs/cern.ch/work/j/jsauvan/public/HTauTau/Trees/mt/151215/'
tree_prod_name = 'H2TauTauTreeProducerTauMu'
data_dir = analysis_dir
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, tree_prod_name=tree_prod_name)
for sample in all_samples:
    setSumWeights(sample, directory='MCWeighter')

mc_info = {}

mc_info['Directory'] = analysis_dir
for sample in all_samples:
    if sample.name!='data_obs':
        mc_info[sample.name] = {'XSec':sample.xsec, 'SumWeights':sample.sumweights}


pickle.dump(mc_info, open('mc_info.pck', 'wb'))


