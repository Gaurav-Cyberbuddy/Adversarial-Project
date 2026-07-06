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

# Load Robust Model

model = SimpleCNN()

model.load_state_dict(
    torch.load("results/adversarial_model.pth")
)

model.eval()

print("Robust Model Loaded Successfully!")

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

criterion = nn.CrossEntropyLoss()

epsilons = [0.01, 0.03, 0.05, 0.10]

print("\nStarting Robust Multi-Epsilon FGSM Evaluation...\n")

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

        adv_images = (
            images +
            epsilon * sign_data_grad
        )

        adv_images = torch.clamp(
            adv_images,
            0,
            1
        )

        adv_outputs = model(
            adv_images
        )

        _, adv_predicted = torch.max(
            adv_outputs,
            1
        )

        total += labels.size(0)

        if adv_predicted.item() == labels.item():
            correct += 1

    accuracy = (
        100 * correct / total
    )

    print(
        f"Epsilon={epsilon:.2f} "
        f"Accuracy={accuracy:.2f}%"
    )

print(
    "\nRobust FGSM Multi-Epsilon Evaluation Complete!"
)