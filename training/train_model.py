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
print("Training Images:", len(trainset))
images, labels = next(iter(trainloader))

print("Image Batch Shape :", images.shape)
print("Label Batch Shape :", labels.shape)
criterion = nn.CrossEntropyLoss()

print("Loss Function:", criterion)

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

print("Optimizer:", optimizer)

print("\nStarting Training...")



epoch_losses = []
epoch_accuracies = []

for epoch in range(10):

    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in trainloader:

        optimizer.zero_grad()

        outputs = model(images)

        _, predicted = torch.max(outputs, 1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    accuracy = 100 * correct / total

    avg_loss = running_loss / len(trainloader)

    epoch_losses.append(avg_loss)
    epoch_accuracies.append(accuracy)

    print(
        f"Epoch {epoch+1} "
        f"Loss: {avg_loss:.4f} "
        f"Accuracy: {accuracy:.2f}%"
    )

print("\nTraining Summary")

for i in range(len(epoch_losses)):

    print(
        f"Epoch {i+1}: "
        f"Loss={epoch_losses[i]:.4f} "
        f"Accuracy={epoch_accuracies[i]:.2f}%"
    )
    torch.save(
    model.state_dict(),
    "results/cnn_model.pth"
)

print("\nModel Saved Successfully!")