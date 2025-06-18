#include "poisson_encoder.h"
#include <cstdlib>  // For rand()
#include <ctime>    // For seeding rand()

void poisson_encode(float image[IMG_HEIGHT][IMG_WIDTH], int spike_train[INPUT_NEURONS][TIME_STEPS]) {
    std::srand(42); // Optional: Seed for reproducibility

    for (int i = 0; i < IMG_HEIGHT; i++) {
        for (int j = 0; j < IMG_WIDTH; j++) {
            int index = i * IMG_WIDTH + j;
            float rate = image[i][j];  // Expecting value in [0, 1]

            for (int t = 0; t < TIME_STEPS; t++) {
                float rand_val = (float) std::rand() / RAND_MAX;
                spike_train[index][t] = (rand_val < rate) ? 1 : 0;
            }
        }
    }
}
