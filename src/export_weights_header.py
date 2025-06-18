# export_weights_header.py
import torch

model_weights = torch.load("../model_weights.pth", map_location='cpu')
weight_matrix = model_weights['net.1.weight']  # Shape: [10, 784]

with open("../model_weights.h", "w") as f:
    f.write("#ifndef MODEL_WEIGHTS_H\n#define MODEL_WEIGHTS_H\n\n")
    f.write("const float model_weights[10][784] = {\n")
    for row in weight_matrix:
        f.write("    {" + ', '.join([f"{w:.6f}" for w in row.tolist()]) + "},\n")
    f.write("};\n\n#endif")
