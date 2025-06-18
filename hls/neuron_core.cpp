// neuron_core.cpp
#include "neuron_core.h"
#include "model_weights.h"
#include <cmath>

// Top-level function for HLS synthesis
void snn_infer(const float input[784], float output[10]) {
    #pragma HLS INTERFACE mode=ap_memory port=input
    #pragma HLS INTERFACE mode=ap_memory port=output
    #pragma HLS INTERFACE mode=ap_ctrl_hs port=return

    #pragma HLS ARRAY_PARTITION variable=model_weights complete dim=1

    // Loop over output neurons
    for (int i = 0; i < 10; i++) {
        #pragma HLS UNROLL
        float sum = 0.0f;

        // Dot product with input
        for (int j = 0; j < 784; j++) {
            #pragma HLS PIPELINE II=1
            sum += model_weights[i][j] * input[j];
        }

        // Simple ReLU activation
        output[i] = (sum > 0) ? sum : 0.0f;
    }
}
