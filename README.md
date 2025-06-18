# Spiking Neural Network Implementation on FPGA

This is an FPGA imlementation of Spiking Neural Network Algorithm that supports simple image classification example.

## Built With

- [scikit-learn](https://scikit-learn.org/stable/install.html)
- [Numpy](https://numpy.org/install/)
- [Matplotlib](https://matplotlib.org/stable/index.html)
- [spikingjelly](https://pypi.org/project/spikingjelly/)

### Getting Started

#### Prerequisites

- Python version 2.9.0 >

  ```sh
  https://www.python.org/
  ```

- Virtualenv

  ```sh
  https://pypi.org/project/virtualenv/
  ```

#### Installation

1. Clone the repository

   ```sh
   git clone https://github.com/Albert-Osei/SNN-implementation.git
   ```

2. Create Virtual Environment

   ```sh
   virtualenv .spike-venv
   ```

   OR


   ```sh
   python -m venv venv
   ```

3. Activate Virtual Environment

   ```sh
   source venv\scripts\activate ~ on~windows
   ```

   ```sh
   source venv/bin/. activate ~ on~mac
   ```

4. Install Dependencies

   ```sh
   pip install -r requirements.txt
   ```

#### Running

* cd into the root where the project is cloned
* run src/inference.py
* this command will use pregenerated weights and output the results of classifying the test images

### Weight Reconstruction (Training)

* to reconstruct the weights, run src/train.py
* this command will generate new or update the model_weights.pth file to be used for prediction in the inference.py