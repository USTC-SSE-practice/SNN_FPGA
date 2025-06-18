# src/train_model.py

import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from spikingjelly.activation_based import neuron, surrogate
import os

# 1. Load MNIST Dataset
def load_mnist(data_dir, batch_size):
    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    train_dataset = datasets.MNIST(
        root=data_dir, train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST(
        root=data_dir, train=False, download=True, transform=transform)

    # Added num_workers=0 here
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    return train_loader, test_loader

# 2. Define the simple SNN model
class SimpleSNN(nn.Module):
    def __init__(self, tau=2.0):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28 * 28, 10, bias=False),
            neuron.LIFNode(tau=tau, surrogate_function=surrogate.ATan())
        )

    def forward(self, x):
        # Reset neuron states before forward
        for module in self.net:
            if hasattr(module, 'reset'):
                module.reset()
        return self.net(x)

# 3. Train function
def train(model, device, train_loader, optimizer, criterion):
    model.train()
    total_loss = 0
    correct = 0
    batch_count = 0  # add a counter

    for data, target in train_loader:
        batch_count += 1
        # Print every 10 batches only to reduce spam
        if batch_count % 10 == 0:
            print(f"Processed {batch_count} batches")
        
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * data.size(0)
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()

    avg_loss = total_loss / len(train_loader.dataset)
    accuracy = correct / len(train_loader.dataset)
    return avg_loss, accuracy

# 4. Test function
def test(model, device, test_loader, criterion):
    model.eval()
    total_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)
            total_loss += loss.item() * data.size(0)
            pred = output.argmax(dim=1)
            correct += pred.eq(target).sum().item()

    avg_loss = total_loss / len(test_loader.dataset)
    accuracy = correct / len(test_loader.dataset)
    return avg_loss, accuracy

# Main script
if __name__ == "__main__":
    data_dir = "../data/mnist"
    batch_size = 64
    epochs = 5
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    train_loader, test_loader = load_mnist(data_dir, batch_size)
    model = SimpleSNN(tau=2.0).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    best_test_acc = 0
    for epoch in range(epochs):
        train_loss, train_acc = train(model, device, train_loader, optimizer, criterion)
        test_loss, test_acc = test(model, device, test_loader, criterion)

        if test_acc > best_test_acc:
            best_test_acc = test_acc
            # Save best weights
            torch.save(model.state_dict(), "../model_weights.pth")

        print(f"Epoch {epoch+1}/{epochs} | "
              f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | "
              f"Test Loss: {test_loss:.4f} | Test Acc: {test_acc:.4f} | "
              f"Best Test Acc: {best_test_acc:.4f}")
