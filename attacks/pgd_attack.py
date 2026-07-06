"""Evaluate baseline CNN under PGD at multiple epsilon values."""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

from attacks.attack_utils import generate_pgd
from models.cnn_model import SimpleCNN

EPSILONS = [0.01, 0.03, 0.05, 0.10]
PGD_STEPS = 10
MODEL_PATH = "results/cnn_model.pth"


def evaluate_pgd(model_path: str = MODEL_PATH) -> None:
    model = SimpleCNN()
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()

    transform = transforms.ToTensor()
    testset = torchvision.datasets.CIFAR10(
        root="./dataset", train=False, download=True, transform=transform
    )
    testloader = torch.utils.data.DataLoader(testset, batch_size=1, shuffle=False)

    criterion = nn.CrossEntropyLoss()
    print(f"\nPGD evaluation ({PGD_STEPS} steps) — {model_path}\n")

    for epsilon in EPSILONS:
        correct = 0
        total = 0
        for images, labels in testloader:
            perturbed = generate_pgd(
                model, images, labels, epsilon=epsilon, steps=PGD_STEPS, criterion=criterion
            )
            with torch.no_grad():
                outputs = model(perturbed)
                predicted = outputs.argmax(dim=1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        accuracy = 100.0 * correct / total
        print(f"Epsilon={epsilon:.2f}  PGD Accuracy={accuracy:.2f}%")


if __name__ == "__main__":
    evaluate_pgd()
