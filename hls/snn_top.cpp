#include "snn_top.h"
#include "poisson_encoder.h"
#include "neuron_core.h"
#include "model_weights.h"

#define IMG_WIDTH 28
#define IMG_HEIGHT 28
#define INPUT_NEURONS (IMG_WIDTH * IMG_HEIGHT)
#define OUTPUT_NEURONS 10
#define TIME_STEPS 100

void snn_top(float input_image[IMG_HEIGHT][IMG_WIDTH], int output_spike_count[OUTPUT_NEURONS]) {
    // Spike train: [INPUT_NEURONS][TIME_STEPS]
    int spike_train[INPUT_NEURONS][TIME_STEPS];

    // Step 1: Poisson encoding
    poisson_encode(input_image, spike_train);

    // Step 2: Run neuron core
    neuron_core(spike_train, model_weights, output_spike_count);
}

