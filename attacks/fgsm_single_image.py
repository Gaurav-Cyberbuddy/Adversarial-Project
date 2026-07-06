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

model.load_state_dict(
    torch.load("results/cnn_model.pth")
)

model.eval()

print("Model Loaded Successfully!")
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
images, labels = next(iter(testloader))
images.requires_grad = True

print("Image Shape:", images.shape)
print("Label:", labels.item())
outputs = model(images)

_, predicted = torch.max(outputs, 1)

print("Predicted Class:", predicted.item())
criterion = nn.CrossEntropyLoss()

loss = criterion(
    outputs,
    labels
)

print("Loss:", loss.item())
model.zero_grad()

loss.backward()
epsilon = 0.03
print(
    "Gradient Shape:",
    images.grad.shape
)
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
adv_output = model(
    perturbed_image
)

_, adv_prediction = torch.max(
    adv_output,
    1
)

print(
    "Adversarial Prediction:",
    adv_prediction.item()
)