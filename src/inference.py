import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from spikingjelly.activation_based import neuron, surrogate

# Use the same SimpleSNN model definition (copy from train.py)
class SimpleSNN(nn.Module):
    def __init__(self, tau=2.0):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28 * 28, 10, bias=False),
            neuron.LIFNode(tau=tau, surrogate_function=surrogate.ATan())
        )

    def forward(self, x):
        for module in self.net:
            if hasattr(module, 'reset'):
                module.reset()
        return self.net(x)

def load_mnist_test(data_dir, batch_size=64):
    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    test_dataset = datasets.MNIST(root=data_dir, train=False, download=True, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return test_loader

def run_inference(model, device, test_loader):
    model.eval()
    model.to(device)

    with torch.no_grad():
        for idx, (data, target) in enumerate(test_loader):
            data, target = data.to(device), target.to(device)
            output = model(data)
            pred = output.argmax(dim=1)

            print(f"Batch {idx+1} predictions: {pred.cpu().numpy()}")
            print(f"Batch {idx+1} ground truths: {target.cpu().numpy()}")

            # Just test one batch for quick verification, then stop
            break

if __name__ == "__main__":
    data_dir = "../data/mnist"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleSNN(tau=2.0)
    model.load_state_dict(torch.load("../model_weights.pth", map_location=device))

    test_loader = load_mnist_test(data_dir)
    run_inference(model, device, test_loader)
