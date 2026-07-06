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
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

from models.cnn_model import SimpleCNN

# Load Model

model = SimpleCNN()

model.load_state_dict(
    torch.load("results/cnn_model.pth")
)

model.eval()

print("Model Loaded Successfully!")

# Dataset

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

classes = [
    "Airplane",
    "Auto",
    "Bird",
    "Cat",
    "Deer",
    "Dog",
    "Frog",
    "Horse",
    "Ship",
    "Truck"
]

true_labels = []
pred_labels = []

with torch.no_grad():

    for images, labels in testloader:

        outputs = model(images)

        _, predicted = torch.max(
            outputs,
            1
        )

        true_labels.extend(
            labels.numpy()
        )

        pred_labels.extend(
            predicted.numpy()
        )

cm = confusion_matrix(
    true_labels,
    pred_labels
)

plt.figure(figsize=(10,8))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=classes
)

disp.plot(
    xticks_rotation=45
)

plt.title(
    "CNN Confusion Matrix"
)

plt.savefig(
    "results/confusion_matrix.png"
)

plt.close()

print(
    "Confusion Matrix Saved!"
)