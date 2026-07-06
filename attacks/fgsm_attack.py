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
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

from models.cnn_model import SimpleCNN

# Load Model
model = SimpleCNN()

model.load_state_dict(
    torch.load("results/cnn_model.pth")
)

model.eval()

print("Model Loaded Successfully!")

# Load Test Dataset
transform = transforms.ToTensor()

testset = torchvision.datasets.CIFAR10(
    root="./dataset",
    train=False,
    download=True,
    transform=transform
)

testloader = torch.utils.data.DataLoader(
    testset,
    batch_size=1,
    shuffle=False
)

print("Test Dataset Loaded!")

# FGSM Strength
epsilon = 0.03

criterion = nn.CrossEntropyLoss()

epsilons = [0.01, 0.03, 0.05, 0.10]

print("\nStarting Multi-Epsilon FGSM Evaluation...\n")

for epsilon in epsilons:

    correct = 0
    total = 0

    for images, labels in testloader:

        images.requires_grad = True

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        model.zero_grad()

        loss.backward()

        data_grad = images.grad.data

        sign_data_grad = data_grad.sign()

        perturbed_image = (
            images +
            epsilon * sign_data_grad
        )

        perturbed_image = torch.clamp(
            perturbed_image,
            0,
            1
        )

        adv_outputs = model(
            perturbed_image
        )

        _, adv_predicted = torch.max(
            adv_outputs,
            1
        )

        total += labels.size(0)

        if adv_predicted.item() == labels.item():
            correct += 1

    fgsm_accuracy = (
        100 * correct / total
    )

    print(
        f"Epsilon={epsilon:.2f} "
        f"Accuracy={fgsm_accuracy:.2f}%"
    )

print("\nFGSM Multi-Epsilon Evaluation Complete!")