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

# Create Model

model = SimpleCNN()

print(model)

transform = transforms.ToTensor()

trainset = torchvision.datasets.CIFAR10(
    root="./dataset",
    train=True,
    download=True,
    transform=transform
)

trainloader = torch.utils.data.DataLoader(
    trainset,
    batch_size=32,
    shuffle=True
)

print(
    "Training Images:",
    len(trainset)
)

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

print(
    "Loss Function:",
    criterion
)

print(
    "Optimizer:",
    optimizer
)

epsilon = 0.03

print(
    "FGSM Strength:",
    epsilon
)

print("\nStarting Improved Adversarial Training...")

for epoch in range(10):

    running_loss = 0.0

    for images, labels in trainloader:

        images.requires_grad = True

        # -------------------
        # Generate FGSM Images
        # -------------------

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

        # -------------------
        # Train Model
        # -------------------

        optimizer.zero_grad()

        clean_outputs = model(images)

        clean_loss = criterion(
            clean_outputs,
            labels
        )

        adv_outputs = model(
            adv_images
        )

        adv_loss = criterion(
            adv_outputs,
            labels
        )

        total_loss = (
            clean_loss +
            adv_loss
        ) / 2

        total_loss.backward()

        optimizer.step()

        running_loss += total_loss.item()

    print(
        f"Epoch {epoch+1} "
        f"Loss: {running_loss/len(trainloader):.4f}"
    )

print("\nImproved Adversarial Training Complete!")

torch.save(
    model.state_dict(),
    "results/adversarial_model.pth"
)

print(
    "Improved Robust Model Saved!"
)