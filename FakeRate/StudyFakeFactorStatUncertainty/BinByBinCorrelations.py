import ROOT
import math
import array

def retrieveAndCheckHisto(inFile,histoName):
    histo = inFile.Get(histoName)
    if not histo:
        raise StandardError("ERROR: cannot find histo "+histoName+" in file "+inFile.GetName())
    histo.__class__ =  ROOT.TH1F
    histo.SetDirectory(0)
    #histo.SetName(newName)
    return histo

def sumHistos(files, histoNames):
    histoSum = None
    for file,histoName in zip(files,histoNames):
        histo = retrieveAndCheckHisto(file, histoName)
        if not histoSum: 
            histoSum = histo.Clone(histo.GetName()+'_sum')
            histoSum.__class__ = ROOT.TH1F
            histoSum.SetDirectory(0)
        else: histoSum.Add(histo)
    return histoSum

def computeShift(hNominal, hSys, name):
    if len(hSys)>2:
        raise StandardError("ERROR: more that 2 shifts for a given source")
    hShift = hNominal.Clone(name)
    hShift.__class__ = ROOT.TH1F
    hShift.SetDirectory(0)
    nbins = hShift.GetNbinsX()
    for b in range(1,nbins+1):
        sysSym = 0.
        nom = hNominal.GetBinContent(b)
        if len(hSys)==2:
            sys1 = hSys[0].GetBinContent(b)
            sys2 = hSys[1].GetBinContent(b)
            sysSym = (abs(sys1-nom) + abs(sys2-nom))/2.
            if sys1-nom<0:
                sysSym = -sysSym
        if len(hSys)==1:
            sysSym = hSys[0].GetBinContent(b)-nom
        hShift.SetBinContent(b,sysSym)
        hShift.SetBinError(b,0.)
    return hShift

class CorrelationMatrix:
    def setPlotStyle(self):
        ROOT.gROOT.SetStyle("Plain");
        ROOT.gStyle.SetOptStat();
        ROOT.gStyle.SetOptFit(0);
        ROOT.gStyle.SetOptTitle(0);
        ROOT.gStyle.SetFrameLineWidth(1);
        ROOT.gStyle.SetPadBottomMargin(0.13);
        ROOT.gStyle.SetPadLeftMargin(0.13);
        ROOT.gStyle.SetPadTopMargin(0.02);
        ROOT.gStyle.SetPadRightMargin(0.13);

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
        ROOT.gStyle.SetTitleOffset(1.2,"Y");
        ROOT.gStyle.SetOptStat(0);
        ROOT.gStyle.SetPalette(1);
        ROOT.gStyle.SetPaintTextFormat("3.2f")
        ROOT.gROOT.ForceStyle();

    def __init__(self):
        self.setPlotStyle()
        self.name = ""
        self.plotDir = 'plots/'
        self.inputFiles = None
        self.histoNames = ""
        self.nomName = ""
        self.sysNames = []
        self.nomHisto = None
        self.sysHistos = []
        self.shiftHistos = []
        self.matrix = None
        self.bounds = []
        self.log = False
        self.title = ""
        self.plotNumbers = False

    def retrieveHistos(self):
        self.nomHisto = sumHistos(self.inputFiles, [f if self.nomName=='' else self.nomName+'/'+h for h in self.histoNames])
        for sysList in self.sysNames:
            if len(sysList)>2:
                raise StandardError("ERROR: More than 2 components for one systematic source")
            sysHistos = []
            for sys in sysList:
                sysHistos.append(sumHistos(self.inputFiles, [sys+"/"+h for h in self.histoNames]))
            self.sysHistos.append(sysHistos)

    def computeShifts(self):
        for sysHistos in self.sysHistos:
            shiftHistos = []
            self.shiftHistos.append(computeShift(self.nomHisto,sysHistos,sysHistos[0].GetName()+"_shift"))

    def computeCorrelationMatrix(self):
        nbins = self.nomHisto.GetNbinsX()
        edges = []
        for b in range(1,nbins+1):
            edge = self.nomHisto.GetXaxis().GetBinLowEdge(b)
            edges.append(edge)
        edges.append(self.nomHisto.GetXaxis().GetBinUpEdge(nbins))
        self.matrix = ROOT.TH2F(self.histoNames[0]+"_corr",self.histoNames[0],nbins,array.array('f',edges),nbins,array.array('f',edges))
        for i in range(1,nbins+1):
            for j in range(1,nbins+1):
                covii=0.
                covjj=0.
                covij=0.
                for shiftHisto in self.shiftHistos:
                    ui = shiftHisto.GetBinContent(i)
                    uj = shiftHisto.GetBinContent(j)
                    covii += ui*ui
                    covjj += uj*uj
                    covij += ui*uj
                if covij!=0.:
                    self.matrix.SetBinContent(i,j,covij/math.sqrt(covii*covjj));
                else:
                    self.matrix.SetBinContent(i,j,0.);

    def plot(self):
        self.setPlotStyle()
        canvas = ROOT.TCanvas(self.name+"_canvas", self.name+"_canvas", 800, 700)
        canvas.SetLogx(self.log)
        canvas.SetLogy(self.log)
        self.matrix.SetXTitle(self.title)
        self.matrix.SetYTitle(self.title)
        self.matrix.SetContour(99)
        if len(self.bounds)==2:
            self.matrix.SetAxisRange(self.bounds[0],self.bounds[1], "X")
            self.matrix.SetAxisRange(self.bounds[0],self.bounds[1], "Y")
        self.matrix.SetAxisRange(-1,1, "Z")
        if not self.plotNumbers:
            self.matrix.Draw("col z")
        else:
            self.matrix.Draw("col z text")
        canvas.Print(self.plotDir+"/binCorrelations_"+self.name+".png")
        canvas.Print(self.plotDir+"/binCorrelations_"+self.name+".pdf")
        canvas.Print(self.plotDir+"/binCorrelations_"+self.name+".eps")
        canvas.Print(self.plotDir+"/binCorrelations_"+self.name+".C")
        return canvas
