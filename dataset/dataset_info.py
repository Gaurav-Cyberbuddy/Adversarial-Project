import torchvision
import torchvision.transforms as transforms

transform = transforms.ToTensor()

trainset = torchvision.datasets.CIFAR10(
    root='./dataset',
    train=True,
    download=True,
    transform=transform
)

testset = torchvision.datasets.CIFAR10(
    root='./dataset',
    train=False,
    download=True,
    transform=transform
)

print("Training Images :", len(trainset))
print("Testing Images  :", len(testset))

print("\nClasses:")

for idx, class_name in enumerate(trainset.classes):
    print(idx, "->", class_name)