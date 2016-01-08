import ROOT
import numpy as np



class VariableCorrelations:
    def __init__(self):
        self.variable_list = []
        self.data = []
        self.corr = None
        
    def setPlotStyle(self):
        ROOT.gROOT.SetStyle("Plain");
        ROOT.gStyle.SetOptStat(0);
        ROOT.gStyle.SetOptFit(0);
        ROOT.gStyle.SetOptTitle(0);
        ROOT.gStyle.SetFrameLineWidth(1);
        ROOT.gStyle.SetPadBottomMargin(0.12);
        ROOT.gStyle.SetPadLeftMargin(0.12);
        ROOT.gStyle.SetPadTopMargin(0.03);
        ROOT.gStyle.SetPadRightMargin(0.12);

        ROOT.gStyle.SetLabelFont(42,"X");
        ROOT.gStyle.SetLabelFont(42,"Y");
        ROOT.gStyle.SetLabelSize(0.05,"X");
        ROOT.gStyle.SetLabelSize(0.05,"Y");
        ROOT.gStyle.SetLabelOffset(0.01,"Y");
        ROOT.gStyle.SetTickLength(0.04,"X");
        ROOT.gStyle.SetTickLength(0.04,"Y");
        ROOT.gStyle.SetLineWidth(1);
        ROOT.gStyle.SetTickLength(0.04 ,"Z");

        ROOT.gStyle.SetTitleSize(0.1);
        ROOT.gStyle.SetTitleFont(42,"X");
        ROOT.gStyle.SetTitleFont(42,"Y");
        ROOT.gStyle.SetTitleSize(0.05,"X");
        ROOT.gStyle.SetTitleSize(0.05,"Y");
        ROOT.gStyle.SetTitleOffset(1.1,"X");
        ROOT.gStyle.SetTitleOffset(1.3,"Y");
        ROOT.gStyle.SetPalette(1);
        ROOT.gStyle.SetPaintTextFormat("3.2f")
        ROOT.gROOT.ForceStyle();


    def readTree(self, tree, cuts):
        ## Apply cuts to read entries
        tree.SetBranchStatus("*", True)
        tree.Draw(">>elist", cuts, "entrylist")
        entry_list = ROOT.gDirectory.Get("elist")
        entry_list.__class__ = ROOT.TEntryList
        entries = entry_list.GetN()
        tree.SetEntryList(entry_list) 
        ## Read only needed variables
        tree.SetBranchStatus("*", False)
        for var in self.variable_list:
            tree.SetBranchStatus(var, True)
        ## Define TTreeFormulas
        formulas = []
        for var in self.variable_list:
            formulas.append(ROOT.TTreeFormula(var,var,tree))
        ## Initialize data
        for var in self.variable_list:
            self.data.append([])
        for entry in xrange(entries):
            if entry%10000==0: print 'Entry {0}/{1}'.format(entry,entries)
            tree_entry = entry_list.GetEntry(entry)
            tree.GetEntry(tree_entry)
            for i,formula in enumerate(formulas):
                formula.GetNdata()
                #print formula.GetName(), formula.EvalInstance()
                self.data[i].append(formula.EvalInstance())
        entry_list.Delete()

    def plotCorrelations(self, name, plotDir='plots/'):
        self.setPlotStyle()
        self.corr = np.corrcoef(self.data)
        corr_histo = ROOT.TH2F(name, name, len(self.variable_list), 0, len(self.variable_list), len(self.variable_list), 0, len(self.variable_list))
        for b in xrange(1, corr_histo.GetNbinsX()+1):
            corr_histo.GetXaxis().SetBinLabel(b, self.variable_list[b-1])
            corr_histo.GetYaxis().SetBinLabel(b, self.variable_list[b-1])
        corr_histo.SetAxisRange(-1,1, 'Z')
        for irow,row in enumerate(self.corr):
            for icolumn,value in enumerate(row):
                corr_histo.SetBinContent(irow+1,icolumn+1,value)
        canvas = ROOT.TCanvas('c'+name, name, 800, 700)
        corr_histo.Draw('col z')
        canvas.Print(plotDir+'/'+name+'.png')

    def plotDependency(self, name, variable1, variable2, n1,  n2, plotDir='plots/'):
        index1 = self.variable_list.index(variable1)
        index2 = self.variable_list.index(variable2)
        min1 = min(self.data[index1])
        max1 = max(self.data[index1])
        min2 = min(self.data[index2])
        max2 = max(self.data[index2])
        dependency = ROOT.TH2F(name+'_'+variable1+'_'+variable2, name+'_'+variable1+'_'+variable2, n1, min1, max1, n2, min2, max2)
        dependency.SetXTitle(variable1)
        dependency.SetYTitle(variable2)
        for v1,v2 in zip(self.data[index1], self.data[index2]):
            dependency.Fill(v1,v2)
        canvas = ROOT.TCanvas('c'+name+'_'+variable1+'_'+variable2, name, 800, 700)
        dependency.Draw('col z')
        canvas.Print(plotDir+'/'+name+'_'+variable1+'_'+variable2+'.png')


