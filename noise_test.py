from noise_test_plot_maker import MakePlot
file_name = "TrackerHistos_10.root"
make_plot = MakePlot()
print(make_plot.save_plot_from_root(file_name))
