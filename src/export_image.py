import os
from torchvision import datasets, transforms

def export_mnist_image_txt(data_dir, index, filename):
    transform = transforms.Compose([transforms.ToTensor()])
    test_dataset = datasets.MNIST(root=data_dir, train=False, download=True, transform=transform)

    # Get the image and label at the specified index
    image, label = test_dataset[index]

    # Flatten the image tensor and convert to a list of floats
    flattened = image.view(-1).tolist()

    # Write to text file with space-separated floats
    with open(filename, 'w') as f:
        f.write(' '.join(str(pixel) for pixel in flattened))

    print(f"Exported image {index} (label: {label}) to {filename}")

if __name__ == "__main__":
    data_dir = "../data/mnist"
    output_file = "../data/sample_input.txt"
    export_mnist_image_txt(data_dir, index=0, filename=output_file)
