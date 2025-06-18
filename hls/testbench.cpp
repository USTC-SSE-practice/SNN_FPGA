#include <iostream>
#include <fstream>
#include <string>
#include "neuron_core.h"

int main() {
    float input[784];
    float output[10];

    // Open the input file
    std::ifstream infile("sample_input.txt");
    if (!infile) {
        std::cerr << "Cannot open input file!" << std::endl;
        return 1;
    }

    // Read 784 float values from file
    for (int i = 0; i < 784; i++) {
        infile >> input[i];
    }
    infile.close();

    // Run inference
    snn_infer(input, output);

    // Print the output neuron values
    std::cout << "Output neuron values:" << std::endl;
    for (int i = 0; i < 10; i++) {
        std::cout << "Neuron " << i << ": " << output[i] << std::endl;
    }

    return 0;
}
