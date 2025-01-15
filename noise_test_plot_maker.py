import ROOT
import sys
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)


class MakePlot():
    def __init__(self) -> None:
        pass
    def save_plot_from_root(self,filename):
        out_file_url = []
        try:
            filename_ = ROOT.TFile(filename)
        except:
            print(f"failed to open {filename}")
            return None
        sides = ["R", "L"]
        folderList = [x.GetName() for x in filename_.GetListOfKeys()]
        print(folderList)
        folderList = [folder for folder in folderList if "Detector" not in folder]
        if not folderList:
            print(" the folder is empty, can't produce the images")
        for folder in folderList:
            
            for i in range(2):
                evenHist = filename_.Get(f"{folder}/Detector/Board_0/OpticalGroup_0/Hybrid_{i}/D_B(0)_O(0)_HybridNoiseEvenDistribution_Hybrid({i})")
                oddHist = filename_.Get(f"{folder}/Detector/Board_0/OpticalGroup_0/Hybrid_{i}/D_B(0)_O(0)_HybridNoiseOddDistribution_Hybrid({i})")

                try:
                    evenHist.GetTitle()
                except:
                    print(f"evenHist is empty for {filename}")
                    return


                canvas = ROOT.TCanvas("", "", 0, 0, 600, 500)
                legend = ROOT.TLegend(0.7, 0.8, 0.89, 0.89)
                legend.SetBorderSize(0)
                # Hybrid 0 even = 2, Hybrid 0 odd = 4
                # Hybrid 1 even = 1, Hybrid 1 odd = 3
                if i == 0:
                    evenHist.SetLineColor(ROOT.kRed)  # bottom right side
                    oddHist.SetLineColor(ROOT.kBlue)  # top right side
                elif i == 1:
                    evenHist.SetLineColor(ROOT.kBlack)  # bottom left side
                    oddHist.SetLineColor(ROOT.kGreen)   # top left side
                evenHist.SetMaximum(20.)
                evenHist.SetTitle(evenHist.GetTitle().replace("Even", ""))
                evenHist.GetYaxis().SetTitle("Noise (V_{CTH})")
                evenHist.GetXaxis().SetTitle("Channel #")
                evenHist.Draw()
                oddHist.Draw("same")
                legend.AddEntry(evenHist, "Bot" + sides[i], "l")
                legend.AddEntry(oddHist, "Top" + sides[i], "l")
                legend.Draw()
    
                outCanvasName = filename.replace(".root", f"_{folder}_FEH{i}")
                #print("save the file no")
                file_url = f"NOISE_TEST_IMAGE_{outCanvasName}.png"
                canvas.SaveAs(file_url)
                out_file_url.append(file_url)
                #canvas.SaveAs(f"{outCanvasName}.pdf")
                #canvas.SaveAs(f"{outCanvasName}.root")
                #canvas.SaveAs(f"{outCanvasName}.C")
                return out_file_url

