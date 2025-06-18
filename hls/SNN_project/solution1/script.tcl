############################################################
## This file is generated automatically by Vitis HLS.
## Please DO NOT edit it.
## Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
############################################################
open_project SNN_project
set_top snn_infer
add_files model_weights.h
add_files neuron_core.cpp
add_files neuron_core.h
add_files ../data/sample_input.txt
add_files -tb testbench.cpp
open_solution "solution1" -flow_target vivado
set_part {xczu7ev-ffvc1156-2-e}
create_clock -period 10 -name default
#source "./SNN_project/solution1/directives.tcl"
csim_design
csynth_design
cosim_design
export_design -format ip_catalog
