import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import torch
import torchvision
import torchvision.transforms as transforms

from models.cnn_model import SimpleCNN

# Create model
model = SimpleCNN()

# Load saved weights
model.load_state_dict(
    torch.load("results/cnn_model.pth")
)

model.eval()

print("Model Loaded Successfully!")

# Test dataset
transform = transforms.ToTensor()

testset = torchvision.datasets.CIFAR10(
    root="./dataset",
    train=False,
    download=True,
    transform=transform
)

testloader = torch.utils.data.DataLoader(
    testset,
    batch_size=32,
    shuffle=False
)

correct = 0
total = 0

with torch.no_grad():

    for images, labels in testloader:

        outputs = model(images)

        _, predicted = torch.max(outputs, 1)

        total += labels.size(0)

        correct += (
            predicted == labels
        ).sum().item()

accuracy = 100 * correct / total

print(
    f"\nTest Accuracy: {accuracy:.2f}%"
)