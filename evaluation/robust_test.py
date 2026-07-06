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

# Load Robust Model
model = SimpleCNN()

model.load_state_dict(
    torch.load("results/adversarial_model.pth")
)

model.eval()

print("Robust Model Loaded Successfully!")

# Test Dataset
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
    f"\nRobust Model Accuracy: {accuracy:.2f}%"
)