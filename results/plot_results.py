import matplotlib.pyplot as plt

# -----------------------------
# Graph 1: Training Accuracy
# -----------------------------

epochs = [1,2,3,4,5,6,7,8,9,10]

accuracies = [
    52.07,
    66.89,
    73.68,
    78.80,
    83.86,
    88.29,
    92.09,
    94.73,
    95.91,
    96.59
]

plt.figure(figsize=(8,5))
plt.plot(epochs, accuracies, marker='o')
plt.title("Training Accuracy vs Epoch")
plt.xlabel("Epoch")
plt.ylabel("Accuracy (%)")
plt.grid(True)
plt.savefig("results/epoch_accuracy.png")
plt.close()

# -----------------------------
# Graph 2: FGSM Comparison
# -----------------------------

models = [
    "CNN",
    "Adversarial CNN"
]

fgsm_acc = [
    7.34,
    29.04
]

plt.figure(figsize=(8,5))
plt.bar(models, fgsm_acc)
plt.title("FGSM Accuracy Comparison")
plt.ylabel("Accuracy (%)")
plt.savefig("results/fgsm_comparison.png")
plt.close()

# -----------------------------
# Graph 3: Epsilon Analysis
# -----------------------------

epsilons = [
    0.01,
    0.03,
    0.05,
    0.10
]

cnn_acc = [
    23.13,
    7.34,
    3.35,
    1.04
]

robust_acc = [
    39.17,
    29.04,
    21.17,
    9.25
]

plt.figure(figsize=(8,5))

plt.plot(
    epsilons,
    cnn_acc,
    marker='o',
    label='CNN'
)

plt.plot(
    epsilons,
    robust_acc,
    marker='o',
    label='Adversarial CNN'
)

plt.title("FGSM Robustness vs Epsilon")
plt.xlabel("Epsilon")
plt.ylabel("Accuracy (%)")
plt.legend()
plt.grid(True)

plt.savefig(
    "results/epsilon_comparison.png"
)

plt.close()

print("Graphs Generated Successfully!")