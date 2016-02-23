import math
import ROOT

class DefaultSysCalculator():
    def __init__(self):
       pass

    def getSystematics(self, nominal, systematics):
        if len(systematics)==0:
            print "[Warning] DefaultSysCalculator.getSystematics(): no systematics given. Returning 0."
            return (None, None)

        if systematics[0].__class__ is ROOT.TH1F:
            return self.getHistoSystematics(nominal, systematics)


    def getHistoSystematics(self, nominal, systematics):
        nBins = nominal.GetNbinsX()
        for sys in systematics:
            if sys.GetNbinsX()!=nBins:
                raise Exception("[ Error ] DefaultSysCalculator.getHistoSystematics(): Cannot combine systematic histos with different number of bins.")

        histoUp = nominal.Clone()
        histoUp.__class__ = ROOT.TH1F
        histoUp.SetName(nominal.GetName()+"_Up")
        histoDown = nominal.Clone()
        histoDown.__class__ = ROOT.TH1F
        histoDown.SetName(nominal.GetName()+"_Down")

        print len(systematics)
        for bin in range(0,nBins+2):
            print "Bin", bin
            sysValueUp = 0
            sysValueDown = 0
            for sys in systematics:
                if sys.GetBinContent(bin)>nominal.GetBinContent(bin):
                    uncert = sys.GetBinContent(bin) - nominal.GetBinContent(bin)
                    sysValueUp +=  uncert**2
                else:
                    uncert = nominal.GetBinContent(bin) - sys.GetBinContent(bin)
                    sysValueDown += uncert**2

            sysValueDown = math.sqrt(sysValueDown)
            sysValueUp = math.sqrt(sysValueUp)
            print sysValueDown, sysValueUp, nominal.GetBinContent(bin)
            histoUp.SetBinContent(bin, histoUp.GetBinContent(bin)+sysValueUp)
            histoDown.SetBinContent(bin, histoDown.GetBinContent(bin)-sysValueDown)

        return (histoDown, histoUp)
