import ROOT


plot_dir = 'results_qcd_vs_muoniso'
input_file = ROOT.TFile.Open('results_qcd_vs_muoniso/nonClosures.root')

data_os = input_file.Get('FFOS_QCD_OS_Data_Histo_Smooth_Ratio_histo')
data_os.__class__ = ROOT.TH1F
data_ss = input_file.Get('FFSS_QCD_SS_Data_Histo_Smooth_Ratio_histo')
data_ss.__class__ = ROOT.TH1F

data_os_sidebands = input_file.Get('FFOS_QCD_OS_mvis_sidebands_Data_Histo_Smooth_Ratio_histo')
data_os_sidebands.__class__ = ROOT.TH1F
data_ss_sidebands = input_file.Get('FFSS_QCD_SS_mvis_sidebands_Data_Histo_Smooth_Ratio_histo')
data_ss_sidebands.__class__ = ROOT.TH1F

mc_os = input_file.Get('FFOS_QCD_OS_MC_Histo_Smooth_Ratio_histo')
mc_os.__class__ = ROOT.TH1F
mc_ss = input_file.Get('FFSS_QCD_SS_MC_Histo_Smooth_Ratio_histo')
mc_ss.__class__ = ROOT.TH1F

def setPlotStyle():
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetOptStat()
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetFrameLineWidth(1)
    ROOT.gStyle.SetPadBottomMargin(0.13)
    ROOT.gStyle.SetPadLeftMargin(0.13)
    ROOT.gStyle.SetPadTopMargin(0.05)
    ROOT.gStyle.SetPadRightMargin(0.03)

    ROOT.gStyle.SetLabelFont(42,"X")
    ROOT.gStyle.SetLabelFont(42,"Y")
    ROOT.gStyle.SetLabelSize(0.04,"X")
    ROOT.gStyle.SetLabelSize(0.04,"Y")
    ROOT.gStyle.SetLabelOffset(0.01,"Y")
    ROOT.gStyle.SetTickLength(0.03,"X")
    ROOT.gStyle.SetTickLength(0.03,"Y")
    ROOT.gStyle.SetLineWidth(1)
    ROOT.gStyle.SetTickLength(0.04 ,"Z")

    ROOT.gStyle.SetTitleSize(0.1)
    ROOT.gStyle.SetTitleFont(42,"X")
    ROOT.gStyle.SetTitleFont(42,"Y")
    ROOT.gStyle.SetTitleSize(0.07,"X")
    ROOT.gStyle.SetTitleSize(0.07,"Y")
    ROOT.gStyle.SetTitleOffset(0.8,"X")
    ROOT.gStyle.SetTitleOffset(0.9,"Y")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetPaintTextFormat("3.2f")
    ROOT.gROOT.ForceStyle()



setPlotStyle()
## Data, OS vs SS
canvas_data = ROOT.TCanvas('data_os_ss', '', 800, 800)
data_os.SetMarkerStyle(20)
data_ss.SetMarkerStyle(24)
data_os.SetAxisRange(0.5, 2.0, 'Y')
data_os.SetXTitle('iso(#mu)')
data_os.SetYTitle('True / Estimated')
data_os.Draw()
data_ss.Draw('same')
legend_data = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
legend_data.SetLineColor(0)
legend_data.SetFillColor(0)
legend_data.AddEntry(data_os, 'Data, OS', 'lp')
legend_data.AddEntry(data_ss, 'Data, SS', 'lp')
legend_data.Draw()
canvas_data.Print(plot_dir+'/FF_QCD_OS_SS_Data_Standard_NonClosure.png')

## Data in sidebands, OS vs SS
canvas_data_sidebands = ROOT.TCanvas('data_os_ss_sidebands', '', 800, 800)
data_os_sidebands.SetMarkerStyle(20)
data_ss_sidebands.SetMarkerStyle(24)
data_os_sidebands.SetAxisRange(0.5, 2.0, 'Y')
data_os_sidebands.SetXTitle('iso(#mu)')
data_os_sidebands.SetYTitle('True / Estimated')
data_os_sidebands.Draw()
data_ss_sidebands.Draw('same')
legend_data_sidebands = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
legend_data_sidebands.SetLineColor(0)
legend_data_sidebands.SetFillColor(0)
legend_data_sidebands.AddEntry(data_os_sidebands, 'Data, OS', 'lp')
legend_data_sidebands.AddEntry(data_ss_sidebands, 'Data, SS', 'lp')
legend_data_sidebands.Draw()
canvas_data_sidebands.Print(plot_dir+'/FF_QCD_OS_SS_sidebands_Data_Standard_NonClosure.png')

## MC, OS vs SS
canvas_mc = ROOT.TCanvas('mc_os_ss', '', 800, 800)
mc_os.SetMarkerStyle(20)
mc_ss.SetMarkerStyle(24)
mc_os.SetAxisRange(0.5, 2.0, 'Y')
mc_os.SetXTitle('iso(#mu)')
mc_os.SetYTitle('True / Estimated')
mc_os.Draw()
mc_ss.Draw('same')
legend_mc = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
legend_mc.SetLineColor(0)
legend_mc.SetFillColor(0)
legend_mc.AddEntry(mc_os, 'MC, OS', 'lp')
legend_mc.AddEntry(mc_ss, 'MC, SS', 'lp')
legend_mc.Draw()
canvas_mc.Print(plot_dir+'/FF_QCD_OS_SS_MC_Standard_NonClosure.png')


input_file.Close()



