// neuron_core.h
#ifndef NEURON_CORE_H
#define NEURON_CORE_H

#define INPUT_NEURONS 784
#define OUTPUT_NEURONS 10
#define TIME_STEPS 100

void neuron_core(
    int spike_train[INPUT_NEURONS][TIME_STEPS],
    const float weights[OUTPUT_NEURONS][INPUT_NEURONS],
    int output_spike_count[OUTPUT_NEURONS]
);

void snn_infer(const float input[784], float output[10]);

#endif

