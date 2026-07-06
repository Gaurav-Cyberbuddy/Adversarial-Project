import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt


transform = transforms.ToTensor()

trainset = torchvision.datasets.CIFAR10(
    root='./dataset',
    train=True,
    download=True,
    transform=transform
)


trainloader = torch.utils.data.DataLoader(
    trainset,
    batch_size=4,
    shuffle=True
)

classes = (
    'plane',
    'car',
    'bird',
    'cat',
    'deer',
    'dog',
    'frog',
    'horse',
    'ship',
    'truck'
)


dataiter = iter(trainloader)
images, labels = next(dataiter)


img = images[0].permute(1, 2, 0)

plt.imshow(img)
plt.title(classes[labels[0]])
plt.axis("off")
plt.show()