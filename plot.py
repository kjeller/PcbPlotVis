from pcbnew import *
import os
import argparse

parser = argparse.ArgumentParser("pcbplotvis")
parser.add_argument("kicad_pcb_filepath", help="KiCad PCB project path (.kicad_pcb)", type=str)
args = parser.parse_args()

kicad_pcb_filepath = args.kicad_pcb_filepath
kicad_project_name = os.path.basename(args.kicad_pcb_filepath).partition('.')[0]
kicad_project_root_path = os.path.dirname(args.kicad_pcb_filepath)

output_dir="plotvis"
pcbplotvis_output_path = os.path.join(kicad_project_root_path, output_dir)
front_layer_output_path = os.path.join(pcbplotvis_output_path, "front_layer_output.png")
back_layer_output_path = os.path.join(pcbplotvis_output_path, "back_layer_output.png")
combined_layers_output_path = os.path.join(pcbplotvis_output_path, "all_layer_output.png")

print("PCB FILEPATH " + kicad_pcb_filepath)
print("PRJECT NAME " + kicad_project_name)
print("ROOT PATH " + kicad_project_root_path)
print("PLOT OUTPUT " + pcbplotvis_output_path)
print("FRONT OUTPUT PATH "+ front_layer_output_path)
print("BACK OUT "+ back_layer_output_path)
#   exit(0)

board = LoadBoard(kicad_pcb_filepath)
pctl = PLOT_CONTROLLER(board)

popt = pctl.GetPlotOptions()
popt.SetOutputDirectory(output_dir)

popt.SetPlotFrameRef(False)
popt.SetSketchPadLineWidth(FromMM(3.))

front_layer_filenames = {
    F_Cu : "layer_F_Cu",
    F_SilkS:  "layer_F_SilkS",
    F_Mask:  "layer_F_Mask",
    Edge_Cuts:  "layer_Edge_Cuts",
}

back_layer_filenames = {
    B_Cu:  "layer_B_Cu",
    B_SilkS:  "layer_B_SilkS",
    B_Mask:  "layer_B_Mask",
    Edge_Cuts:  "layer_Edge_Cuts_back",
}

layer_colors = {
    F_Cu : "#000000",
    F_SilkS:  "#FFFFFF",
    F_Mask:  "#e84b02",
    B_Cu:  "#000000",
    B_SilkS:  "#FFFFFF",
    B_Mask:  "#e84b02",
    Edge_Cuts:  "#000000",
}

for layer, layer_name in front_layer_filenames.items():
    pctl.SetLayer(layer)
    svg_filename = f"{layer_name}"
    pctl.OpenPlotfile(svg_filename, PLOT_FORMAT_SVG, f"SVG File for {layer_name}")
    pctl.PlotLayer()
    pctl.ClosePlot()

popt.SetMirror(True)

for layer, layer_name in back_layer_filenames.items():
    pctl.SetLayer(layer)
    svg_filename = f"{layer_name}"
    pctl.OpenPlotfile(svg_filename, PLOT_FORMAT_SVG, f"SVG File for {layer_name}")
    pctl.PlotLayer()
    pctl.ClosePlot()

print("Layer plotting complete.")

# Generate png from svg and color
for layer, layer_name in front_layer_filenames.items() | back_layer_filenames.items():
    svg_path = os.path.join(pcbplotvis_output_path, "{}-{}.svg".format(kicad_project_name, layer_name))
    os.system("inkscape -z --export-type=\"png\" --export-dpi=300 {}".format(svg_path))
    png_path = os.path.join(pcbplotvis_output_path, "{}-{}.png".format(kicad_project_name, layer_name))
    os.system("mogrify -fuzz 100%% -fill \"{}\" -opaque black {}".format(layer_colors[layer], png_path))

# Merge all layers and create output image
merge_layers_front =[
    [F_Cu, F_Mask, F_SilkS],
    [B_Cu, B_Mask, B_SilkS]
]
front_filepaths = ''.join(["{}/{}-{}.png ".format(pcbplotvis_output_path, kicad_project_name, front_layer_filenames[f]) for f in merge_layers_front[0]])
back_filepaths = ''.join(["{}/{}-{}.png ".format(pcbplotvis_output_path, kicad_project_name, back_layer_filenames[f]) for f in merge_layers_front[1]])

os.system("convert {} -gravity center -background none -layers merge -trim {}".format(front_filepaths, front_layer_output_path))
os.system("convert {} -gravity center -background none -layers merge -trim {}".format(back_filepaths, back_layer_output_path))
os.system("convert +append {} {} {}".format(front_layer_output_path, back_layer_output_path, combined_layers_output_path))
     