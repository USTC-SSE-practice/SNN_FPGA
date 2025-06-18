#ifndef POISSON_ENCODER_H
#define POISSON_ENCODER_H

#define IMG_WIDTH 28
#define IMG_HEIGHT 28
#define INPUT_NEURONS (IMG_WIDTH * IMG_HEIGHT)
#define TIME_STEPS 100

// Main interface function
void poisson_encode(float image[IMG_HEIGHT][IMG_WIDTH], int spike_train[INPUT_NEURONS][TIME_STEPS]);

#endif
