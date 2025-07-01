#include <iostream>
#include <fstream>
#include <xrt/xrt_device.h>   
#include <xrt/xrt_kernel.h>   
#include <xrt/xrt_bo.h>       
#include <vector>
#include <cstring>

#define IMG_WIDTH 28
#define IMG_HEIGHT 28
#define INPUT_NEURONS (IMG_WIDTH * IMG_HEIGHT)
#define OUTPUT_NEURONS 10

int main(int argc, char* argv[]) {
    std::cout << "SNN Host Application (ZCU104)" << std::endl;

    // Load input image
    float input_image[IMG_HEIGHT][IMG_WIDTH];
    std::ifstream infile("sample_input.txt");
    if (!infile) {
        std::cerr << "Failed to open input file!" << std::endl;
        return 1;
    }
    for (int i = 0; i < IMG_HEIGHT; i++) {
        for (int j = 0; j < IMG_WIDTH; j++) {
            infile >> input_image[i][j];
        }
    }
    infile.close();

    // Convert 2D to 1D array 
    std::vector<float> input_data(INPUT_NEURONS);
    for (int i = 0; i < IMG_HEIGHT; ++i)
        for (int j = 0; j < IMG_WIDTH; ++j)
            input_data[i * IMG_WIDTH + j] = input_image[i][j];

    std::vector<int> output_data(OUTPUT_NEURONS, 0);

    // Load FPGA binary (xclbin)
    std::string binaryFile = "snn_top.xclbin";
    xrt::device device(0);
    xrt::uuid uuid = device.load_xclbin(binaryFile);
    xrt::kernel kernel = xrt::kernel(device, uuid, "snn_top");

    // Allocate device memory
    xrt::bo input_bo = xrt::bo(device, input_data.size() * sizeof(float), kernel.group_id(0));
    xrt::bo output_bo = xrt::bo(device, output_data.size() * sizeof(int), kernel.group_id(1));

    // Copy input data to device
    input_bo.write(input_data.data());
    input_bo.sync(XCL_BO_SYNC_BO_TO_DEVICE);

    // Run kernel
    auto run = kernel(input_bo, output_bo);
    run.wait();

    // Copy result back to host
    output_bo.sync(XCL_BO_SYNC_BO_FROM_DEVICE);
    output_bo.read(output_data.data());

    std::cout << "FPGA kernel execution complete." << std::endl;
    std::cout << "Output spike counts:" << std::endl;
    for (int i = 0; i < OUTPUT_NEURONS; ++i) {
        std::cout << "Class " << i << ": " << output_data[i] << std::endl;
    }

    return 0;
}
