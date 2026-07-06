"""Shared helpers for FGSM and PGD attacks."""

import torch
import torch.nn as nn


def generate_fgsm(
    model: nn.Module,
    images: torch.Tensor,
    labels: torch.Tensor,
    epsilon: float,
    criterion: nn.Module | None = None,
) -> torch.Tensor:
    """Single-step FGSM perturbation with L-infinity clamping to [0, 1]."""
    if criterion is None:
        criterion = nn.CrossEntropyLoss()

    images = images.clone().detach().requires_grad_(True)
    outputs = model(images)
    loss = criterion(outputs, labels)
    model.zero_grad()
    loss.backward()

    perturbed = images + epsilon * images.grad.sign()
    return torch.clamp(perturbed, 0.0, 1.0).detach()


def generate_pgd(
    model: nn.Module,
    images: torch.Tensor,
    labels: torch.Tensor,
    epsilon: float,
    alpha: float | None = None,
    steps: int = 10,
    criterion: nn.Module | None = None,
) -> torch.Tensor:
    """PGD-Linf attack (Madry et al.): iterative signed gradient steps."""
    if criterion is None:
        criterion = nn.CrossEntropyLoss()
    if alpha is None:
        alpha = epsilon / 4.0

    original = images.clone().detach()
    perturbed = original.clone()

    for _ in range(steps):
        perturbed = perturbed.clone().detach().requires_grad_(True)
        outputs = model(perturbed)
        loss = criterion(outputs, labels)
        model.zero_grad()
        loss.backward()

        with torch.no_grad():
            perturbed = perturbed + alpha * perturbed.grad.sign()
            perturbed = torch.max(
                torch.min(perturbed, original + epsilon),
                original - epsilon,
            )
            perturbed = torch.clamp(perturbed, 0.0, 1.0)

    return perturbed.detach()
