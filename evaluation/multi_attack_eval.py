"""Run FGSM and PGD on baseline and robust checkpoints; export CSV."""

import csv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

from attacks.attack_utils import generate_fgsm, generate_pgd
from models.cnn_model import SimpleCNN

EPSILONS = [0.01, 0.03, 0.05, 0.10]
PGD_STEPS = 10
CHECKPOINTS = {
    "standard": "results/cnn_model.pth",
    "robust": "results/adversarial_model.pth",
}
OUTPUT_CSV = "results/attack_benchmark.csv"


def accuracy_under_attack(
    model: nn.Module,
    attack: str,
    epsilon: float,
    testloader,
    criterion: nn.Module,
) -> float:
    correct = 0
    total = 0
    for images, labels in testloader:
        if attack == "fgsm":
            perturbed = generate_fgsm(model, images, labels, epsilon, criterion)
        elif attack == "pgd":
            perturbed = generate_pgd(
                model, images, labels, epsilon, steps=PGD_STEPS, criterion=criterion
            )
        else:
            raise ValueError(f"Unknown attack: {attack}")

        with torch.no_grad():
            predicted = model(perturbed).argmax(dim=1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    return 100.0 * correct / total


def main() -> None:
    transform = transforms.ToTensor()
    testset = torchvision.datasets.CIFAR10(
        root="./dataset", train=False, download=True, transform=transform
    )
    testloader = torch.utils.data.DataLoader(testset, batch_size=1, shuffle=False)
    criterion = nn.CrossEntropyLoss()

    rows = []
    for model_name, path in CHECKPOINTS.items():
        model = SimpleCNN()
        model.load_state_dict(torch.load(path, map_location="cpu"))
        model.eval()

        for attack in ("fgsm", "pgd"):
            for epsilon in EPSILONS:
                acc = accuracy_under_attack(model, attack, epsilon, testloader, criterion)
                rows.append(
                    {
                        "model": model_name,
                        "attack": attack,
                        "epsilon": epsilon,
                        "accuracy_pct": round(acc, 2),
                    }
                )
                print(
                    f"{model_name:8s}  {attack:4s}  eps={epsilon:.2f}  acc={acc:.2f}%"
                )

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["model", "attack", "epsilon", "accuracy_pct"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved benchmark to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
