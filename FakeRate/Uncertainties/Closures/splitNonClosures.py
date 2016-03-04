import ROOT


def split(graph, cuts):
    i = 0
    graphs = []
    for cut1,cut2 in zip(cuts[:-1],cuts[1:]):
        graphcopy = graph.Clone(graph.GetName()+'_'+str(i))
        graphcopy.__class__ = ROOT.TGraphAsymmErrors
        p1 = 0
        p2 = 0
        for p in xrange(graphcopy.GetN()):
            x = graphcopy.GetX()[p]
            if p1 is 0 and x>cut1: p1=p
            if p2 is 0 and x>cut2: p2=p
            if x<cut1 or x>cut2:
                graphcopy.SetPoint(p,x,1)
        if i>0:
            graphcopy.SetPoint(p1-1, cut1-0.0001,1)
            graphcopy.SetPoint(p1, cut1+0.0001,graph.Eval(cut1+0.0001))
        if i<len(cuts)-2:
            graphcopy.SetPoint(p2-1, cut2-0.0001, graph.Eval(cut2-0.0001))
            graphcopy.SetPoint(p2, cut2+0.0001, 1)
        graphs.append(graphcopy)
        i+=1
    return graphs



inputs = [
    ('results/nonClosures.root'   , 'HighMT_Histo_Smooth_Ratio'),
    ('results/nonClosures.root'   , 'QCDSS_Histo_Smooth_Ratio'),
    ('results/nonClosures_SS.root', 'HighMTSS_Histo_Smooth_Ratio'),
]

cuts = [0,50,100,200,1000]

output = ROOT.TFile.Open('results/nonClosures_split.root', 'RECREATE')

for filename,graphname in inputs:
    file = ROOT.TFile.Open(filename)
    graph = file.Get(graphname)
    graph.__class__ = ROOT.TGraphAsymmErrors
    graphs = split(graph,cuts)
    output.cd()
    for g in graphs:
        g.Write()
    file.Close()

output.Close()




