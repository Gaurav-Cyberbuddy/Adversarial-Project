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
import matplotlib.pyplot as plt

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

image, label = testset[0]

image = image.unsqueeze(0)

image.requires_grad = True

# Original Prediction

output = model(image)

_, predicted = torch.max(
    output,
    1
)

print(
    "Original Prediction:",
    predicted.item()
)

# FGSM Attack

criterion = nn.CrossEntropyLoss()

loss = criterion(
    output,
    torch.tensor([label])
)

model.zero_grad()

loss.backward()

epsilon = 0.03

data_grad = image.grad.data

adv_image = (
    image +
    epsilon * data_grad.sign()
)

adv_image = torch.clamp(
    adv_image,
    0,
    1
)

# Adversarial Prediction

adv_output = model(
    adv_image
)

_, adv_predicted = torch.max(
    adv_output,
    1
)

print(
    "Adversarial Prediction:",
    adv_predicted.item()
)

# Save Figure

fig, axes = plt.subplots(
    1,
    2,
    figsize=(8,4)
)

axes[0].imshow(
    image.squeeze().permute(1,2,0).detach().numpy()
)

axes[0].set_title(
    f"Original\nPred={predicted.item()}"
)

axes[0].axis("off")

axes[1].imshow(
    adv_image.squeeze().permute(1,2,0).detach().numpy()
)

axes[1].set_title(
    f"Adversarial\nPred={adv_predicted.item()}"
)

axes[1].axis("off")

plt.tight_layout()

plt.savefig(
    "results/adversarial_example.png"
)

plt.close()

print(
    "Adversarial Example Saved!"
)