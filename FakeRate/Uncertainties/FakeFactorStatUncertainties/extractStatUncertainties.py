import ROOT
from array import array


def extract1DGraphUncert(graph, point):
    xs = []
    ysup = []
    ysdown = []
    for p in graph.GetN():
        xs.append(graph.GetX()[p])
        ysup.append(graph.GetEhighY()[p] if p==point else 0)
        ysdown.append(graph.GetElowY()[p] if p==point else 0)
    graphup = ROOT.TGraphAsymmErrors(len(xs), array('f',xs), array('f',ysup), array('f',[0]*len(xs)), array('f',[0]*len(xs)), array('f',[0]*len(xs)), array('f',[0]*len(xs)))
    graphdown = ROOT.TGraphAsymmErrors(len(xs), array('f',xs), array('f',ysdown), array('f',[0]*len(xs)), array('f',[0]*len(xs)), array('f',[0]*len(xs)), array('f',[0]*len(xs)))
    graphup.SetName(graph.GetName()+'_'+str(point)+'_StatUp')
    graphdown.SetName(graph.GetName()+'_'+str(point)+'_StatDown')
    return graphup,graphdown


def extract2DHistoUncert(histo, bin1, bin2):
    histoup = histo.Clone(histo.GetName()+'_'+str(bin1)+'_'+str(bin2)+'_StatUp')
    histodown = histo.Clone(histo.GetName()+'_'+str(bin1)+'_'+str(bin2)+'_StatDown')
    nbinsx = histo.GetNbinsX()
    nbinsy = histo.GetNbinsY()
    for bx in xrange(0,nbinsx+2): 
        for by in xrange(0,nbinsy+2):
            up = 0.
            down = 0.
            if bx==bin1 and by==bin2:
                up = histo.GetBinError(bx,by)
                down = -histo.GetBinError(bx,by)
                content = histo.GetBinContent(bx,by)
                # avoid negative fake factors
                if content+down<0: down = -content
            histoup.SetBinContent(bx,by,up)
            histodown.SetBinContent(bx,by,down)
            histoup.SetBinError(bx,by,0)
            histodown.SetBinError(bx,by,0)
    return histoup, histodown



base_dir = '/home/sauvan/Documents/HEP/Projects/CMS/Htautau_Run2/Studies/FakeRate/ComputeFakeRates/plots/'
fake_factors = ['HighMT', 'QCDSS', 'ZMuMu']
histos2D = []
for fake_factor in fake_factors:
    for data_mc in ['_Data','']:
        histos2D.append(
            {
                'File':'{DIR}/FakeFactors{DATA}_{FACTOR}_2D/FakeFactors{DATA}_{FACTOR}_2D.root'.format(DIR=base_dir,DATA=data_mc,FACTOR=fake_factor),
                'Histos':['FakeFactors{DATA}_{FACTOR}_2D_Iso_Medium_InvertIso_Medium_tau_pt_vs_decayMode'.format(DATA=data_mc,FACTOR=fake_factor)],
            }
        )

bins = {
    'tau_pt_vs_decayMode':[[],[1,2,11]]
}


for histo2D in histos2D:
    print '> File '+histo2D['File']
    file = ROOT.TFile.Open(histo2D['File'])
    histos = []
    for histo in histo2D['Histos']:
        histos.append(file.Get(histo))
    outfile = ROOT.TFile('results/'+histo2D['File'].split('/')[-1].replace('.root', '_StatShift.root'), 'RECREATE')
    for histo in histos:
        binsx = []
        binsy = []
        for vars,blist in bins.items():
            if vars in histo.GetName():
                binsx = blist[0]
                binsy = blist[1]
        ## if zero bins take all the bins
        if len(binsx)==0: binsx = range(0,histo.GetNbinsX()+2)
        if len(binsy)==0: binsy = range(0,histo.GetNbinsY()+2)
        histosShift = []
        for bx in binsx:
            for by in binsy:
                histosShift.append(extract2DHistoUncert(histo,bx,by))
        for histoup,histodown in histosShift:
            histoup.Draw('colz')
            histodown.Draw('colz')
            histoup.Write()
            histodown.Write()
    file.Close()
    outfile.Close()

